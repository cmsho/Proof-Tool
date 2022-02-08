from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from proofchecker.models import Proof, ProofLine, Problem, Assignment, StudentAssignment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import AssignmentForm


class AssignmentListView(ListView):
    model = Assignment
    template_name = "assignments/assignments.html"


class AssignmentCreateView(CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = "assignments/add_assignment.html"
    success_url = "/assignments/"
