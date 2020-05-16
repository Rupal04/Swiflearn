from django.conf.urls import url
from student_system import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url('create/', views.CreateStudentView.as_view(), name='create'),
    url('authenticate/', obtain_auth_token, name='authenticate'),
    url('assigned_sessions/', views.AssignedSessionView.as_view(), name='assigned_sessions'),
]