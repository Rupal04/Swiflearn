import logging

from django.db.models import Prefetch

from student_system.response import SuccessResponse,ErrorResponse, ServerErrorResponse
from student_system.constant import Success,Error
from student_system.models import Student, AvailableSessions, Question, Classes
from student_system.serializers import StudentSerializer, ClassSerializer, QuestionSerializer
from rest_framework.authtoken.models import Token


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

        sessions_qset = AvailableSessions.objects.filter(grade=user_obj.grade,
                                                         board=user_obj.board).prefetch_related(
                                                         Prefetch('classes', to_attr='sessions_lst',
                                                         queryset=Classes.objects.prefetch_related(
                                                         Prefetch('question',to_attr="related_questions"))))

        result = {"grade": user_obj.grade, "board": user_obj.board}

        if sessions_qset:
            for sess in sessions_qset:
                sessions_list = []
                classes = sess.sessions_lst
                for cls in classes:
                    questions = cls.related_questions
                    qn_list = []
                    if questions:
                        for question in questions:
                            serialized_question = QuestionSerializer(question)
                            qn_list.append(serialized_question.data)

                    session = {"class": cls.session, "date": cls.date, "questions": qn_list}
                    sessions_list.append(session)
            result["sessions"] = sessions_list

            return SuccessResponse(msg=Success.CLASSES_FETCHED_SUCCESS, results=result)

        else:
            return SuccessResponse(msg=Error.NO_CLASSES_AVAILABLE)

    except Exception as e:
        logger.error(Error.SESSION_FETCHING_ERROR + str(e))
        return None