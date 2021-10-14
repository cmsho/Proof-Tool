from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from proofchecker.models import Student, Instructor, User


class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()

        student = Student.objects.create(user=user)
        student.save()
        return user


class InstructorSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self):
        user = super().save(commit=False)
        user.is_instructor = True
        user.save()

        instructor = Instructor.objects.create(user=user)
        instructor.save()
        return user
