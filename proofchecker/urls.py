from django.contrib import admin
from django.urls import path

from . import views

admin.site.site_header = "ProofChecker Admin"

urlpatterns = [
    path('', views.home, name='home'),

    path("problems/", views.ProblemView.as_view(), name="all_problems"),
    path("proofs/", views.ProofView.as_view(), name="all_proofs"),
    path("assignments/", views.AssignmentView.as_view(), name="all_assignments"),
    path("assignments/new", views.AssignmentCreateView.as_view(), name="add_assignment"),
    path("assignments/<pk>/update/", views.AssignmentUpdateView.as_view(), name="update_assignment"),
    path("assignments/<pk>/delete/", views.AssignmentDeleteView.as_view(), name="delete_assignment"),
    path("proofs/new/", views.proof_create_view, name="add_proof"),
    path('proofs/<int:pk>/', views.ProofDetailView.as_view(), name='proof_detail'),
    path("proofs/<pk>/update/", views.proof_update_view, name="update_proof"),
    path("proofs/<pk>/delete/", views.ProofDeleteView.as_view(), name="delete_proof"),
    path("proofs/assignmentpage/", views.AssignmentPage, name='assignment_page'),
    path("proofs/checker/", views.proof_checker, name='proof_checker'),
    path("proofs/singleproofchecker",views.single_proof_checker, name='single_proof_checker'),
    path("proofs/syntaxtest",views.SyntaxTestPage,name='syntax_test')
]
