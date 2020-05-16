import logging

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from student_system.response import SuccessResponse,ErrorResponse, ServerErrorResponse
from student_system.constant import Success,Error
from student_system.utility import signup, fetch_user_id_from_token, get_assigned_sessions
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)


class CreateStudentView(APIView):
    """Create a new user in the system"""
    def post(self, request):
        try:
            data = request.data
            response = signup(data)

            if not response:
                response = ErrorResponse(msg=Error.STUDENT_PROFILE_CREATION_ERROR)
                return Response(response.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if response and response.success is False:
                return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)

            return Response(response.__dict__, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(Error.EXCEPTION + str(e))
            response = ServerErrorResponse()
            return Response(response.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AssignedSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = fetch_user_id_from_token(request.auth)

            response = get_assigned_sessions(user_id)

            if not response:
                response = ErrorResponse(msg=Error.CLASSES_FETCHING_ERROR)
                return Response(response.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if response and response.success is False:
                return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)

            return Response(response.__dict__, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(Error.EXCEPTION + str(e))
            response = ServerErrorResponse()
            return Response(response.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






