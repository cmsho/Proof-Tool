from urllib import request
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
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


class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['image', 'mobile']


class InstructorProfileForm(forms.ModelForm):

    class Meta:
        model = Instructor
        fields = ['image', 'mobile']
