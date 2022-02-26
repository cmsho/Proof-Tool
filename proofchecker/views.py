from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory

from accounts.decorators import instructor_required
from proofchecker.utils import tflparser
from proofchecker.utils import folparser
from .forms import ProofCheckerForm, ProofForm, ProofLineForm
from .models import Proof, Problem, Assignment, Instructor, ProofLine, Student
from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import get_premises
from proofchecker.proofs.proofchecker import verify_proof


def home(request):
    proofs = Proof.objects.all()
    context = {"proofs": proofs}
    return render(request, "proofchecker/home.html", context)


def AssignmentPage(request):
    return render(request, "proofchecker/assignment_page.html")


def SyntaxTestPage(request):
    return render(request, "proofchecker/testpages/syntax_test.html")


def proof_checker(request):
    ProofLineFormset = inlineformset_factory(
        Proof, ProofLine, form=ProofLineForm, extra=0, can_order=True)
    query_set = ProofLine.objects.none()
    form = ProofForm(request.POST or None)
    formset = ProofLineFormset(
        request.POST or None, instance=form.instance, queryset=query_set)
    response = None

    if request.POST:
        if all([form.is_valid(), formset.is_valid()]):

            parent = form.save(commit=False)

            if 'check_proof' in request.POST:
                # Create a new proof object
                proof = ProofObj(lines=[])

                # Grab premise and conclusion from the form
                # Assign them to the proof object
                proof.rules = str(parent.rules)
                proof.premises = get_premises(parent.premises)
                proof.conclusion = str(parent.conclusion)

                for line in formset.ordered_forms:
                    if len(line.cleaned_data) > 0 and not line.cleaned_data['DELETE']:
                        # Create a proofline object
                        proofline = ProofLineObj()

                        # Grab the line_no, formula, and expression from the form
                        # Assign them to the proofline object
                        child = line.save(commit=False)
                        child.proof = parent

                        proofline.line_no = str(child.line_no)
                        proofline.expression = str(child.formula)
                        proofline.rule = str(child.rule)

                        # Append the proofline to the proof object's lines
                        proof.lines.append(proofline)

                # Determine which parser to user based on selected rules
                if ((proof.rules == 'fol_basic') or (proof.rules == 'fol_derived')):
                    parser = folparser.parser
                else:
                    parser = tflparser.parser

                # Verify the proof!
                response = verify_proof(proof, parser)

                # Send the response back
                context = {
                    "form": form,
                    "formset": formset,
                    "response": response
                }

                return render(request, 'proofchecker/proof_checker.html', context)

    context = {
        "form": form,
        "formset": formset
    }
    return render(request, 'proofchecker/proof_checker.html', context)


@login_required
def proof_create_view(request):
    ProofLineFormset = inlineformset_factory(
        Proof, ProofLine, form=ProofLineForm, extra=0, can_order=True)
    query_set = ProofLine.objects.none()
    form = ProofForm(request.POST or None)
    formset = ProofLineFormset(
        request.POST or None, instance=form.instance, queryset=query_set)
    response = None

    if request.POST:
        if all([form.is_valid(), formset.is_valid()]):
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
                    return HttpResponseRedirect(reverse('all_proofs'))

    context = {
        "object": form,
        "form": form,
        "formset": formset,
        "response": response
    }
    return render(request, 'proofchecker/proof_add_edit.html', context)


@login_required
def proof_update_view(request, pk=None):
    obj = get_object_or_404(Proof, pk=pk)
    ProofLineFormset = inlineformset_factory(
        Proof, ProofLine, form=ProofLineForm, extra=0, can_order=True)
    form = ProofForm(request.POST or None, instance=obj)
    formset = ProofLineFormset(
        request.POST or None, instance=obj, queryset=obj.proofline_set.order_by("ORDER"))
    response = None
    validation_failure = False

    if request.POST:
        if all([form.is_valid(), formset.is_valid()]):
            parent = form.save(commit=False)
            if 'check_proof' in request.POST:
                proof = ProofObj(lines=[])
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
                    return HttpResponseRedirect(reverse('all_proofs'))

    context = {
        "object": obj,
        "form": form,
        "formset": formset,
        "response": response

    }
    return render(request, 'proofchecker/proof_add_edit.html', context)


class ProofView(LoginRequiredMixin, ListView):
    model = Proof
    template_name = "proofchecker/allproofs.html"
    paginate_by = 8

    def get_queryset(self):
        return Proof.objects.filter(created_by=self.request.user)


class ProofDetailView(DetailView):
    model = Proof


class ProofDeleteView(DeleteView):
    model = Proof
    template_name = "proofchecker/delete_proof.html"
    success_url = "/proofs/"


class ProblemView(ListView):
    model = Problem
    template_name = "proofchecker/problems.html"


@instructor_required
def student_proofs_view(request, pk=None):
    students = Student.objects.all()
    student = None
    proofs = None

    if pk is not None:
        student = Student.objects.get(user__pk=pk)
        proofs = Proof.objects.filter(created_by=pk)

    context = {
        "students": students,
        "student": student,
        "proofs": proofs
    }
    return render(request, 'proofchecker/student_proofs.html', context)
