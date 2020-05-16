import logging

from student_system.response import SuccessResponse, ErrorResponse
from student_system.constant import Success, Error
from student_system.models import Student, AvailableSessions, Classes
from student_system.serializers import StudentSerializer, AvailableSessionsSerializer

from rest_framework.authtoken.models import Token

from django.db.models import Prefetch
from django.contrib.auth import get_user_model
User = get_user_model()


logger = logging.getLogger(__name__)


def signup(data):
    try:
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        age = data.get('age', None)
        city = data.get('city', None)
        grade = data.get('grade', None)
        board = data.get('board', None)

        user_obj = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)

        if user_obj:
            user_obj.set_password(password)
            user_obj.save()

            student_obj = Student.objects.create(user_id=user_obj.id, age=age, city=city, grade=grade, board=board)
            if student_obj:
                serialized_stu_obj = StudentSerializer(student_obj)
                return SuccessResponse(msg=Success.STUDENT_PROFILE_CREATE_SUCCESS, results=serialized_stu_obj.data)
            else:
                return ErrorResponse(msg=Error.STUDENT_PROFILE_CREATION_ERROR)
        else:
            return ErrorResponse(msg=Error.USER_CREATION_ERROR)

    except Exception as e:
        logger.error(Error.USER_CREATION_ERROR + str(e))
        return None


def fetch_user_id_from_token(token):
    try:
        token = Token.objects.get(key=token)
        return token.user_id
    except Exception as e:
        logger.error(Error.USER_ID_FETCH_ERROR + str(e))
        return None


def get_assigned_sessions(user_id):
    try:
        user_obj = Student.objects.get(user_id=user_id)
        available_session_obj = AvailableSessions.objects.filter(grade=user_obj.grade,
                                                                 board=user_obj.board).prefetch_related(
                                                                 Prefetch('classes', to_attr='sessions_lst',
                                                                          queryset=Classes.objects.prefetch_related(
                                                                            Prefetch('questions',
                                                                                     to_attr="related_questions")))
                                                            ).first()
        if available_session_obj:
            classes = available_session_obj.sessions_lst
            for cls in classes:
                class_related_questions = cls.related_questions

                if class_related_questions:
                    for ques in class_related_questions:
                        cls.questions.add(ques)

                available_session_obj.classes.add(cls)
            serialized_session_obj = AvailableSessionsSerializer(available_session_obj)
            return SuccessResponse(msg=Success.CLASSES_FETCHED_SUCCESS, results=serialized_session_obj.data)
        else:
            return SuccessResponse(msg=Error.NO_SESSIONS_AVAILABLE)

    except Exception as e:
        logger.error(Error.CLASSES_FETCHING_ERROR + str(e))
        return None
