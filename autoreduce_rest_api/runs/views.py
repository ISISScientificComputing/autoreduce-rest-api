from typing import Optional
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework import authentication, permissions

from autoreduce_scripts.manual_operations.manual_submission import main as submit_main
from autoreduce_scripts.manual_operations.manual_batch_submit import main as submit_batch_main
from autoreduce_scripts.manual_operations.manual_remove import main as remove_main


def get_common_args_from_request(request):
    """Gets common arguments that are used in all POST views"""
    return (request.data.get("reduction_arguments", {}), request.data.get("user_id",
                                                                          -1), request.data.get("description", ""))


# pylint:disable=no-self-use
class ManageRuns(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, instrument: str):
        """
        Submits the runs via manual submission on a POST request.

        POST data args:
            runs: List of int run numbers to submit
            reduction_arguments: Dictionary of arguments that will be sent in the Message
            user_id: User ID of the user who submitted the runs
            description: Description of the run

        Returns:
            submitted_runs: List of run numbers that were submitted
        """
        if "runs" not in request.data:
            return JsonResponse({"error": "No 'runs' key specified"}, status=400)
        reduction_arguments, user_id, description = get_common_args_from_request(request)
        try:
            submitted_runs = submit_main(instrument,
                                         request.data["runs"],
                                         reduction_script=None,
                                         reduction_arguments=reduction_arguments,
                                         user_id=user_id,
                                         description=description)
            return JsonResponse({"submitted_runs": submitted_runs})
        except RuntimeError as err:
            return JsonResponse({"message": str(err)}, status=400)

    def delete(self, request, instrument: str):
        """
        Delete the runs via manual remove on a DELETE request.

        DELETE data args:
            runs: List of int run numbers to submit

        Returns:
            removed_runs: List of run numbers that were deleted
        """
        if "runs" not in request.data:
            return JsonResponse({"error": "No 'runs' key specified"}, status=400)
        removed_runs = remove_main(instrument, request.data["runs"], delete_all_versions=True, no_input=True)
        return JsonResponse({"removed_runs": removed_runs})


class BatchSubmit(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, instrument: str):
        """
        Submits the runs as a batch reduction

        POST data args:
            runs: List of int run numbers to submit
            reduction_arguments: Dictionary of arguments that will be sent in the Message
            user_id: User ID of the user who submitted the runs
            description: Description of the run

        Returns:
            submitted_runs: List of run numbers that were submitted
        """
        if "runs" not in request.data:
            return JsonResponse({"error": "No 'runs' key specified"}, status=400)
        reduction_arguments, user_id, description = get_common_args_from_request(request)
        try:
            return JsonResponse({
                "submitted_runs":
                submit_batch_main(instrument,
                                  request.data["runs"],
                                  reduction_script=None,
                                  reduction_arguments=reduction_arguments,
                                  user_id=user_id,
                                  description=description)
            })
        except RuntimeError as err:
            return JsonResponse({"message": str(err)}, status=400)

    # pylint:disable=invalid-name
    def delete(self, request, instrument: str):
        """
        Deletes the batch reduction

        DELETE data args:
            runs: List of int run numbers to submit

        Returns:
            removed_runs: List of run numbers that were deleted
        """
        if "runs" not in request.data:
            return JsonResponse({"error": "No 'runs' key specified"}, status=400)
        try:
            return JsonResponse({
                "removed_runs":
                remove_main(instrument, request.data["runs"], delete_all_versions=True, no_input=True, batch=True)
            })
        except RuntimeError as err:
            return JsonResponse({"message": str(err)}, status=400)
