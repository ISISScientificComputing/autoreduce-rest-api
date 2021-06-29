from autoreduce_utils.clients.connection_exception import ConnectionException
import requests
import time
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from rest_framework.authtoken.models import Token

from autoreduce_db.reduction_viewer.models import ReductionRun
from autoreduce_qp.queue_processor.queue_listener import setup_connection


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
        return super().setUpClass()

    def setUp(self) -> None:
        user = get_user_model()
        self.token = Token.objects.create(user=user.objects.first())
        return super().setUp()

    def test_submit_and_delete_run_range(self):
        """
        Submit and delete a run range via the API
        """
        response = requests.post(f"{self.live_server_url}/api/runs/INTER/63125/63130",
                                 headers={"Authorization": f"Token {self.token}"})
        assert response.status_code == 200
        assert wait_until(lambda: ReductionRun.objects.count() == 5)
        response = requests.delete(f"{self.live_server_url}/api/runs/INTER/63125/63130",
                                   headers={"Authorization": f"Token {self.token}"})
        assert response.status_code == 200
        assert wait_until(lambda: ReductionRun.objects.count() == 0)
