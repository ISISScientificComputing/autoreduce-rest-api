from autoreduce_utils.clients.connection_exception import ConnectionException
import requests
import os
import time
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from rest_framework.authtoken.models import Token
from unittest.mock import Mock, patch

from autoreduce_db.reduction_viewer.models import ReductionRun
from autoreduce_qp.queue_processor.queue_listener import setup_connection
from autoreduce_utils.settings import SCRIPTS_DIRECTORY

INSTRUMENT_NAME = "TESTINSTRUMENT"


def wait_until(somepredicate, timeout=30, period=0.25, *args, **kwargs):
    """
    Wait until the condition is True, or it times out
    """
    mustend = time.time() + timeout
    while time.time() < mustend:
        if somepredicate(*args, **kwargs):
            return True
        time.sleep(period)
    return False


class SubmitRunsTest(LiveServerTestCase):
    fixtures = ["autoreduce_rest_api/autoreduce_django/fixtures/super_user_fixture.json"]

    @classmethod
    def setUpClass(cls) -> None:
        try:
            cls.queue_client, cls.listener = setup_connection()
        except ConnectionException as err:
            raise RuntimeError("Could not connect to ActiveMQ - check your credentials. If running locally check that "
                               "ActiveMQ is running and started by `python setup.py start`") from err

        os.makedirs(SCRIPTS_DIRECTORY % INSTRUMENT_NAME, exist_ok=True)
        with open(os.path.join(SCRIPTS_DIRECTORY % INSTRUMENT_NAME, "reduce_vars.py"), 'w') as file:
            file.write("")

        return super().setUpClass()

    def setUp(self) -> None:
        user = get_user_model()
        self.token = Token.objects.create(user=user.objects.first())
        return super().setUp()

    @patch('autoreduce_scripts.manual_operations.manual_submission.login_icat')
    @patch('autoreduce_scripts.manual_operations.manual_submission.get_location_and_rb_from_icat',
           return_value=["/tmp/location", "RB1234567"])
    def test_submit_and_delete_run_range(self, login_icat: Mock, get_location_and_rb_from_icat: Mock):
        """
        Submit and delete a run range via the API
        """
        response = requests.post(f"{self.live_server_url}/api/runs/{INSTRUMENT_NAME}/63125/63130",
                                 headers={"Authorization": f"Token {self.token}"})
        assert response.status_code == 200
        assert wait_until(lambda: ReductionRun.objects.count() == 6)
        login_icat.assert_called_once()
        login_icat.reset_mock()
        assert get_location_and_rb_from_icat.call_count == 5
        get_location_and_rb_from_icat.reset_mock()

        response = requests.delete(f"{self.live_server_url}/api/runs/{INSTRUMENT_NAME}/63125/63130",
                                   headers={"Authorization": f"Token {self.token}"})
        assert response.status_code == 200
        assert wait_until(lambda: ReductionRun.objects.count() == 0)
        login_icat.assert_not_called()
        get_location_and_rb_from_icat.assert_not_called()
