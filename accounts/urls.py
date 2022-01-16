from django.urls import path

from accounts.views import SignUpView, InstructorSignUpView, StudentSignUpView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('accounts/signup/', SignUpView.as_view(), name="signup"),
    path('accounts/signup/student', StudentSignUpView.as_view(), name="student_signup"),
    path('accounts/signup/instructor', InstructorSignUpView.as_view(), name="instructor_signup"),
    
    # Forgot Password 
    path('accounts/reset_password', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('accounts/reset_password/done', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('accounts/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('accounts/reset/done', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]