from typing import Optional
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework import authentication, permissions

from autoreduce_scripts.manual_operations.manual_submission import main as submit_main
from autoreduce_scripts.manual_operations.manual_batch_submit import main as submit_batch_main
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


class BatchSubmit(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, instrument: str):
        """Submits the runs as a batch reduction"""
        if "runs" not in request.data:
            return JsonResponse({"error": "No 'runs' key specified"}, status=400)
        if "reduction_arguments" not in request.data:
            reduction_arguments = {}
        else:
            reduction_arguments = request.data["reduction_arguments"]
        try:
            return JsonResponse(
                {"submitted_runs": submit_batch_main(instrument, request.data["runs"], reduction_arguments)})
        except RuntimeError as err:
            return JsonResponse({"message": str(err)}, status=400)
