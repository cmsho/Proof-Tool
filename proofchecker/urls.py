from django.contrib import admin
from django.urls import path

from . import views

admin.site.site_header = "ProofChecker Admin"

urlpatterns = [
    path('', views.home, name='home'),
    path("proofs/", views.ProofView.as_view(), name="all_proofs"),
    path("proofs/new/", views.proof_create_view, name="add_proof"),
    path('proofs/<int:pk>/', views.ProofDetailView.as_view(), name='proof_detail'),
    path("proofs/<pk>/update/", views.proof_update_view, name="update_proof"),
    path("proofs/<pk>/delete/", views.ProofDeleteView.as_view(), name="delete_proof"),
    path("proofs/assignmentpage/", views.AssignmentPage, name='assignment_page'),
    path("proofs/checker/", views.proof_checker, name='proof_checker'),
    path("tests/syntaxtest", views.SyntaxTestPage, name='syntax_test'),
]
