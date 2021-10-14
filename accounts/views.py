from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import TemplateView

# Create your views here.
from accounts.forms import StudentSignUpForm, InstructorSignUpForm

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
        return redirect('login')
