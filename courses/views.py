from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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
            selected_students = request.POST.getlist('studentsSelector[]')
            course = form.save(commit=False)
            course.instructor = Instructor.objects.get(user_id=request.user)
            course.save()
            course.students.clear()
            for student in selected_students:
                course.students.add(student)
            course.save()
            messages.success(request, f'Course saved successfully')
            return HttpResponseRedirect(reverse('edit_course', kwargs={'pk': course.id}))

    context = {
        "form": form,
        "students": students
    }
    return render(request, "courses/add_course.html", context)


@instructor_required
def course_edit_view(request, pk=None):
    course = get_object_or_404(Course, pk=pk)
    form = CourseCreateForm(request.POST or None, instance=course)
    students = Student.objects.all()

    if request.POST:
        if form.is_valid():
            selected_students = request.POST.getlist('studentsSelector[]')
            course = form.save(commit=False)
            course.instructor = Instructor.objects.get(user_id=request.user)
            course.save()
            course.students.clear()
            for student in selected_students:
                course.students.add(student)
            course.save()
            messages.success(request, f'Course saved successfully')

    selected_students = []
    for student in students:
        if student.course_set.filter(pk=course.pk).exists():
            selected_students.append({'student': student, 'selected': 'selected'})
        else:
            selected_students.append({'student': student, 'selected': None})

    context = {
        "form": form,
        "students": selected_students,
    }
    return render(request, "courses/edit_course.html", context)


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
