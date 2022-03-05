from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from accounts.decorators import instructor_required
from proofchecker.models import Course, Instructor, Student, User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from proofchecker.models import Course, Instructor
from .forms import CourseCreateForm


# Create your views here.

class CourseView(ListView):
    model = Course
    template_name = "courses/allcourses.html"

    def get_queryset(self):
        return Course.objects.filter(instructor__user=self.request.user)



@instructor_required
def course_create_view(request):
    form = CourseCreateForm(request.POST or None)
    students = Student.objects.all()

    if request.POST:
        if form.is_valid():
            # pass
            # title = form.cleaned_data.get('title')
            # term = form.cleaned_data.get('term')
            # section = form.cleaned_data.get('section')
            selected_students = request.POST.getlist('studentsSelector[]')
            course = form.save(commit=False)
            course.instructor = Instructor.objects.get(user_id=request.user)
            course.save()
            course.students.clear()
            for student in selected_students:
                course.students.add(student)
            course.save()

    context = {
        "form": form,
        "students": students
    }
    return render(request, "courses/add_course.html", context)



class CourseCreateView(CreateView):
    model = Course
    form_class = CourseCreateForm
    template_name = "courses/add_course.html"
    success_url = "/courses/"

    def form_valid(self, form):
        form.instance.instructor = Instructor.objects.filter(user=self.request.user).first()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Student.objects.all()
        return context


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseCreateForm
    template_name = "courses/update_course.html"
    success_url = "/courses/"


class CourseDeleteView(DeleteView):
    model = Course
    template_name = "courses/delete_course.html"
    success_url = "/courses/"
