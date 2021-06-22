from typing import Optional
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from autoreduce_scripts.manual_operations.manual_submission import main


class GenerateToken(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    authentication_classes = [authentication.SessionAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return JsonResponse({"message": "hi"})
