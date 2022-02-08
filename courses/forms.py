from django import forms

from proofchecker.models import Course, Instructor, Student


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'term', 'section', 'students']
