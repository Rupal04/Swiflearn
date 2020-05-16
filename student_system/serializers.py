from django.contrib.auth import get_user_model
from rest_framework import serializers
from student_system.models import Student, Classes, Question
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['user']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question']


class ClassSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Classes
        fields = ['question', 'date', 'session']

