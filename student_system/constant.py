class Success(object):
    SUCCESS_RESPONSE = "Successful"
    SUCCESS = "Success"

    STUDENT_PROFILE_CREATE_SUCCESS = "Successfully created user profile."
    CLASSES_FETCHED_SUCCESS = "Successfully fetched sessions and questions."


class Error(object):
    ERROR_RESPONSE = "Error"
    SERVER_ERROR_5XX = "SERVER ERROR"
    EXCEPTION = "Some Unexpected Exception Occurred. Error is "

    STUDENT_PROFILE_CREATION_ERROR = "Error in creating student profile."
    USER_CREATION_ERROR = "Error in creating user."

    USER_ID_FETCH_ERROR = "Error in fetching user id."
    CLASSES_FETCHING_ERROR = "Error in fetching available sessions for that user."

    NO_SESSIONS_AVAILABLE = "There are no sessions available for this board and grade."

