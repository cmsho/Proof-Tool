from django.contrib import admin
from django.urls import path
from . import views

admin.site.site_header = "ProofChecker Admin"

urlpatterns = [
    path("assignments/", views.AssignmentListView.as_view(), name="all_assignments"),
    path("assignments/add", views.AssignmentCreateView.as_view(), name="add_assignment"),

]