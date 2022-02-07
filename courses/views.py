from django.shortcuts import render
from proofchecker.models import Course, Instructor, Student
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import CourseCreateForm
from django.urls import reverse_lazy


# Create your views here.

class CourseView(ListView):
    model = Course
    template_name = "courses/allcourses.html"


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseCreateForm
    template_name = "courses/add_course.html"
    success_url = "/courses"

    def form_valid(self, form):
        form.instance.instructor = Instructor.objects.filter(user=self.request.user).first()
        return super().form_valid(form)


class CourseUpdateView(UpdateView):
    model = Course
    fields = [
        "title",
        "term",
        "section",
        "students",
    ]


class CourseDeleteView(DeleteView):
    model = Course
    template_name = "courses/delete_course.html"

