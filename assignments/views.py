from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from proofchecker.forms import ProofLineForm, ProofForm
from proofchecker.models import Proof, ProofLine, Problem, Assignment, StudentAssignment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from proofchecker.proofs.proofchecker import verify_proof
from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj
from proofchecker.proofs.proofutils import get_premises
from proofchecker.utils import folparser, tflparser
from .forms import AssignmentForm, ProblemForm


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
    ProofLineFormset = inlineformset_factory(Proof, ProofLine, form=ProofLineForm, extra=0, can_order=True)
    query_set = ProofLine.objects.none()
    form = ProblemForm(request.POST or None)
    formset = ProofLineFormset(request.POST or None, instance=form.instance, queryset=query_set)
    response = None

    if request.POST:
        if formset.is_valid():
            parent = form.save(commit=False)

            if 'check_proof' in request.POST:
                proof = ProofObj(lines=[])  #
                proof.rules = str(parent.rules)
                proof.premises = get_premises(parent.premises)
                proof.conclusion = str(parent.conclusion)

                for line in formset.ordered_forms:
                    if len(line.cleaned_data) > 0 and not line.cleaned_data['DELETE']:
                        proofline = ProofLineObj()
                        child = line.save(commit=False)
                        child.proof = parent
                        proofline.line_no = str(child.line_no)
                        proofline.expression = str(child.formula)
                        proofline.rule = str(child.rule)
                        proof.lines.append(proofline)

                # Determine which parser to user based on selected rules
                if ((proof.rules == 'fol_basic') or (proof.rules == 'fol_derived')):
                    parser = folparser.parser
                else:
                    parser = tflparser.parser

                response = verify_proof(proof, parser)

            elif 'submit' in request.POST:
                if len(formset.forms) > 0:
                    parent.created_by = request.user
                    parent.save()
                    formset.save()
                    Problem.objects.create(proof=parent, grade=form.cleaned_data.get("grade"))
                    return HttpResponseRedirect(reverse('all_problems'))

    context = {
        "object": form,
        "form": form,
        "formset": formset,
        "response": response
    }
    return render(request, 'assignments/problem_add_edit.html', context)


class ProblemView(ListView):
    model = Problem
    template_name = "assignments/problems.html"


    # def get_queryset(self):
    #     return Problem.objects.filter(instructor__user=self.request.user)
