from django.contrib import admin
from django.urls import path
from . import views

admin.site.site_header = "ProofChecker Admin"

urlpatterns = [
    path("assignments/", views.AssignmentListView.as_view(), name="all_assignments"),
    path("assignments/add", views.AssignmentCreateView.as_view(), name="add_assignment"),
    path("problems/add", views.create_problem, name="add_problem"),
    path("problems/", views.ProblemView.as_view(), name="all_problems"),
    path('problems/<int:pk>/update', views.problem_update_view, name="edit_problem"),
    path('problems/<int:pk>/delete', views.ProblemDeleteView.as_view(), name="delete_problem"),
]