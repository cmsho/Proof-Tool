from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DeleteView

from proofchecker.forms import ProofLineForm
from proofchecker.models import Proof, ProofLine, Problem, Assignment
from .forms import AssignmentForm, ProblemForm, ProblemProofForm


class AssignmentListView(ListView):
    model = Assignment
    template_name = "assignments/assignments.html"


class AssignmentCreateView(CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = "assignments/add_assignment.html"
    success_url = "/assignments/"


@login_required
def create_problem(request):
    problem_form = ProblemForm(request.POST or None)
    proof_form = ProblemProofForm(request.POST or None)

    query_set = ProofLine.objects.none()
    ProofLineFormset = inlineformset_factory(Proof, ProofLine, form=ProofLineForm, extra=0, can_order=True)
    formset = ProofLineFormset(request.POST or None, instance=proof_form.instance, queryset=query_set)

    if request.POST:
        if all([problem_form.is_valid(), proof_form.is_valid(), formset.is_valid()]):
            problem = problem_form.save(commit=False)
            proof = proof_form.save(commit=False)

            proof.created_by = request.user
            proof.save()
            formset.save()

            problem.proof = proof
            problem.save()
            return HttpResponseRedirect(reverse('all_problems'))

    context = {
        "problem_form": problem_form,
        "proof_form": proof_form,
        "formset": formset
    }
    return render(request, 'assignments/problem_add_edit.html', context)


def problem_update_view(request, pk=None):
    problem = get_object_or_404(Problem, pk=pk)
    problem_form = ProblemForm(request.POST or None, instance=problem)

    proof = Proof.objects.get(problem=problem)
    proof_form = ProblemProofForm(request.POST or None, instance=proof)

    ProofLineFormset = inlineformset_factory(Proof, ProofLine, form=ProofLineForm, extra=0, can_order=True)
    formset = ProofLineFormset(request.POST or None, instance=proof, queryset=proof.proofline_set.order_by("ORDER"))

    if request.POST:
        if all([problem_form.is_valid(), proof_form.is_valid(), formset.is_valid()]):
            problem = problem_form.save(commit=False)
            proof = proof_form.save(commit=False)

            proof.created_by = request.user
            proof.save()
            formset.save()

            problem.proof = proof
            problem.save()
            return HttpResponseRedirect(reverse('all_problems'))

    context = {
        "object": problem,
        "problem_form": problem_form,
        "proof_form": proof_form,
        "formset": formset
    }
    return render(request, 'assignments/problem_add_edit.html', context)


class ProblemView(ListView):
    model = Problem
    template_name = "assignments/problems.html"

    # def get_queryset(self):
    #     return Problem.objects.filter(instructor__user=self.request.user)


class ProblemDeleteView(DeleteView):
    model = Problem
    template_name = "assignments/delete_problem.html"
    success_url = "/problems/"
