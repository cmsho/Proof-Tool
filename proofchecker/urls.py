from django.contrib import admin
from django.urls import path

from . import views

admin.site.site_header = "ProofChecker Admin"

urlpatterns = [
    path('', views.home, name='home'),
    path("proofs/", views.ProofView.as_view(), name="all_proofs"),

    # CRUD
    path("proofs/new/", views.proof_create_view, name="add_proof"),
    path('proofs/<int:id>/', views.proof_detail_view, name='proof_detail'),
    path('proofs/hx/<int:id>/', views.proof_detail_hx_view, name='hx_detail'),
    path("proofs/<id>/update/", views.proof_update_view, name="update_proof"),
    path("proofs/<id>/delete/", views.ProofDeleteView.as_view(), name="delete_proof"),

    # Checkers
    path("proofs/checker/", views.proof_checker, name='proof_checker'),
    path("proofs/singleproofchecker",views.single_proof_checker, name='single_proof_checker'),

    # TODO: Move these all into separate assignments app (not proofchecker)
    path("proofs/assignmentpage/", views.AssignmentPage, name='assignment_page'),
    path("problems/", views.ProblemView.as_view(), name="all_problems"),
    path("assignments/", views.AssignmentView.as_view(), name="all_assignments"),
    path("assignments/new", views.AssignmentCreateView.as_view(), name="add_assignment"),
    path("assignments/<id>/update/", views.AssignmentUpdateView.as_view(), name="update_assignment"),
    path("assignments/<id>/delete/", views.AssignmentDeleteView.as_view(), name="delete_assignment"),
]
