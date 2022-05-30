from django.contrib import admin
from django.urls import path

from . import views

admin.site.site_header = "ProofChecker Admin"

urlpatterns = [
    path("assignments/", views.all_assignments_view, name="all_assignments"),
    path("assignments/add", views.create_assignment_view, name="add_assignment"),
    path('assignment/<int:pk>/details', views.assignment_details_view, name="assignment_details"),
    path('assignment/<int:pk>/delete', views.AssignmentDeleteView.as_view(), name="delete_assignment"),
    path("problems/add", views.create_problem, name="add_problem"),
    path("problems/", views.ProblemView.as_view(), name="all_problems"),
    path('problems/<int:pk>/details', views.problem_details_view, name="problem_details"),
    path('problems/<int:pk>/delete', views.ProblemDeleteView.as_view(), name="delete_problem"),

    path('problems/<int:problem_id>/solution', views.problem_solution_view, name="problem_solution"),
    
    path('get_csv_file/<int:id>/', views.get_csv_file, name='get_csv_file')

]
