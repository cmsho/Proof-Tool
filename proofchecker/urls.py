from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("proofs/", views.ProofView.as_view(), name="all_proofs"),
    path("proofs/new/", views.ProofCreateView.as_view(), name="add_proof"),
    path("proofs/<pk>/update/", views.ProofUpdateView.as_view(), name="update_proof"),
    path("proofs/<pk>/delete/", views.PostDeleteView.as_view(), name="delete_proof"),
    path("proofs/assignmentpage", views.AssignmentPage, name='assignment_page'),
]
