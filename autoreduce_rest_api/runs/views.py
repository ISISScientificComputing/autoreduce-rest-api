from typing import Optional
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework import authentication, permissions

from autoreduce_scripts.manual_operations.manual_submission import main as submit_main
from autoreduce_scripts.manual_operations.manual_remove import main as remove_main


# pylint:disable=no-self-use
class ManageRuns(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def post(self, _, instrument: str, start: int, end: Optional[int] = None):
        """
        Submits the runs via manual submission on a POST request.
        """
        submitted_runs = submit_main(instrument, start, end)
        return JsonResponse({"submitted_runs": submitted_runs})

    def delete(self, _, instrument: str, start: int, end: Optional[int] = None):
        """
        Delete the runs via manual remove on a DELETE request.
        """
        removed_runs = remove_main(instrument, start, end, delete_all_versions=True, no_input=True)
        return JsonResponse({"removed_runs": removed_runs})
