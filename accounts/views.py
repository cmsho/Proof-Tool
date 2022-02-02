from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.contrib import messages

# Create your views here.
from accounts.forms import StudentSignUpForm, InstructorSignUpForm, StudentProfileForm, InstructorProfileForm

User = get_user_model()


class SignUpView(TemplateView):
    template_name = "accounts/signup.html"


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = "accounts/signup_form.html"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Account created for {username}')
        return redirect('login')


class InstructorSignUpView(CreateView):
    model = User
    form_class = InstructorSignUpForm
    template_name = "accounts/signup_form.html"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'instructor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Account created for {username}')
        return redirect('login')


class StudentProfileView(CreateView):
    model = User
    form_class = StudentProfileForm
    template_name = "profiles/student_profile.html"

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        messages.success(
            self.request, f'Profile Updated Successfully for {username}')
        return redirect('student_profile')


class InstructorProfileView(CreateView):
    model = User
    form_class = InstructorProfileForm
    template_name = "profiles/instructor_profile.html"

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        messages.success(
            self.request, f'Profile Updated Successfully for {username}')
        return redirect('instructor_profile')
