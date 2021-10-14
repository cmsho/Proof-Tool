from django.urls import path

from accounts.views import SignUpView, InstructorSignUpView, StudentSignUpView

urlpatterns = [
    path('accounts/signup/', SignUpView.as_view(), name="signup"),
    path('accounts/signup/student', StudentSignUpView.as_view(), name="student_signup"),
    path('accounts/signup/instructor', InstructorSignUpView.as_view(), name="instructor_signup"),

]
