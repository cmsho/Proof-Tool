from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DeleteView

from accounts.decorators import instructor_required
from proofchecker.forms import ProofLineForm
from proofchecker.models import Proof, ProofLine, Problem, Assignment, Instructor, Course, Student, \
    StudentProblemSolution, User
from proofchecker.proofs.proofchecker import verify_proof
from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj
from proofchecker.proofs.proofutils import get_premises
from proofchecker.utils import folparser, tflparser
from .forms import AssignmentForm, ProblemForm, ProblemProofForm, StudentProblemProofForm, StudentProblemForm


@login_required
def all_assignments_view(request):
    if request.user.is_instructor:
        return instructor_assignments_view(request)
    elif request.user.is_student:
        return student_assignments_view(request)


def instructor_assignments_view(request):
    object_list = Assignment.objects.filter(created_by__user=request.user)
    context = {
        "object_list": object_list,
    }
    return render(request, "assignments/instructor_assignments.html", context)


def student_assignments_view(request):
    object_list = Assignment.objects.filter(course__in=Course.objects.filter(Q(students__user=request.user)))
    context = {
        "object_list": object_list,
    }
    return render(request, "assignments/student_assignments.html", context)


#
# @login_required(decorators, name='dispatch')
# class AssignmentListView(ListView):
#     model = Assignment
#     template_name = "assignments/instructor_assignments.html"
#
#     def get_queryset(self):
#         return Assignment.objects.filter(created_by__user=self.request.user)
#


@instructor_required
def create_assignment_view(request):
    form = AssignmentForm(request.POST or None)
    instructor = Instructor.objects.get(user=request.user)

    if request.POST:
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.created_by = instructor
            assignment.save()
            messages.success(request, 'Assignment got created successfully!')

            return HttpResponseRedirect(reverse('assignment_details', kwargs={'pk': assignment.pk}))
        else:
            messages.error(request, form.errors)

    context = {
        "form": form,
    }
    return render(request, 'assignments/add_assignment.html', context)


@login_required
def assignment_details_view(request, pk=None):
    assignment = get_object_or_404(Assignment, pk=pk)
    form = AssignmentForm(request.POST or None, instance=assignment)
    problems = assignment.problems.all()

    if request.POST:
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.problems.add(*problems)
            assignment.save()

            return HttpResponseRedirect(reverse('all_assignments'))
        else:
            messages.error(request, form.errors)

    context = {
        "assignment": assignment,
        "form": form,
        "problems": problems
    }
    return render(request, 'assignments/assignment_details.html', context)


class AssignmentDeleteView(DeleteView):
    model = Assignment
    template_name = "assignments/delete_assignment.html"
    success_url = "/assignments/"


@login_required
def create_problem(request):
    problem_form = ProblemForm(request.POST or None)
    proof_form = ProblemProofForm(request.POST or None)

    query_set = ProofLine.objects.none()
    ProofLineFormset = inlineformset_factory(Proof, ProofLine, form=ProofLineForm, extra=0, can_order=True)
    formset = ProofLineFormset(request.POST or None, instance=proof_form.instance, queryset=query_set)

    assignmentPk = request.GET.get('assignment')
    problem = None

    if request.POST:
        if all([problem_form.is_valid(), proof_form.is_valid(), formset.is_valid()]):
            problem = problem_form.save(commit=False)
            proof = proof_form.save(commit=False)

            proof.created_by = request.user
            proof.save()
            formset.save()

            problem.proof = proof
            problem.save()

            if assignmentPk is not None:
                # problem page loaded from assignment page
                assignment = Assignment.objects.get(id=assignmentPk)
                assignment.problems.add(problem)
                assignment.save()

                return redirect("/assignment/" + assignmentPk + "/details")

            return HttpResponseRedirect(reverse('all_assignments'))

    context = {
        "problem_form": problem_form,
        "proof_form": proof_form,
        "formset": formset
    }
    return render(request, 'assignments/problem_details.html', context)


@login_required
def problem_details_view(request, pk=None):
    problem = get_object_or_404(Problem, pk=pk)
    problem_form = ProblemForm(request.POST or None, instance=problem)

    studentPk = request.GET.get('studentId')
    if studentPk is None:
        if request.user.is_student:
            studentPk = request.user.pk

    assignmentPk = request.GET.get('assignment')
    proof = None
    try:
        solution = StudentProblemSolution.objects.get(student__user_id=studentPk,
                                                      assignment=Assignment.objects.get(id=assignmentPk),
                                                      problem=problem)
        if solution is not None:
            return problem_solution_view(request, problem.id)
    except StudentProblemSolution.DoesNotExist:
        pass

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
            messages.success(request, "Problem saved successfully")

            if assignmentPk is not None:
                # problem page loaded from assignment page
                return redirect("/assignment/" + assignmentPk + "/details")

            return HttpResponseRedirect(reverse('all_assignments'))

    context = {
        "object": problem,
        "problem_form": problem_form,
        "proof_form": proof_form,
        "formset": formset
    }
    return render(request, 'assignments/problem_details.html', context)


@login_required
def problem_solution_view(request, problem_id=None):
    problem = get_object_or_404(Problem, pk=problem_id)
    problem_form = StudentProblemForm(request.POST or None, instance=problem)

    studentPk = request.GET.get('studentId')
    if studentPk is None:
        if request.user.is_student:
            studentPk = request.user.pk

    assignmentPk = request.GET.get('assignment')
    proof = None
    try:
        solution = StudentProblemSolution.objects.get(student__user_id=studentPk, assignment_id=assignmentPk,
                                                      problem_id=problem.id)
        proof = solution.proof
    except StudentProblemSolution.DoesNotExist:
        print("no solution exists")
        problem_proof_id = problem.proof.id
        proof = Proof.objects.get(id=problem_proof_id)
        proof.id = None
        proof.created_by = User.objects.get(pk=studentPk)
        proof.save()

        prooflines = ProofLine.objects.filter(proof_id=problem_proof_id)

        for proofline in prooflines:
            proofline.id = None
            proofline.proof = proof
            proofline.save()

        solution = StudentProblemSolution(student=Student.objects.get(user_id=studentPk),
                                          assignment=Assignment.objects.get(id=assignmentPk),
                                          problem=Problem.objects.get(pk=problem_id),
                                          proof=Proof.objects.get(id=proof.id))
        solution.save()

    proof_form = StudentProblemProofForm(request.POST or None, instance=proof)

    ProofLineFormset = inlineformset_factory(Proof, ProofLine, form=ProofLineForm, extra=0, can_order=True)
    formset = ProofLineFormset(request.POST or None, instance=proof, queryset=proof.proofline_set.order_by("ORDER"))

    response = None
    if request.POST:
        if all([problem_form.is_valid(), proof_form.is_valid(), formset.is_valid()]):
            parent = proof_form.save(commit=False)
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
                proof.save()
                formset.save()
                messages.success(request, "Solution saved successfully")
                return HttpResponseRedirect(reverse('all_assignments'))

    context = {
        "object": problem,
        "problem_form": problem_form,
        "proof_form": proof_form,
        "formset": formset,
        "response": response
    }
    return render(request, 'assignments/problem_solution.html', context)


class ProblemView(ListView):
    model = Problem
    template_name = "assignments/problems.html"

    # def get_queryset(self):
    #     return Problem.objects.filter(instructor__user=self.request.user)


class ProblemDeleteView(DeleteView):
    model = Problem
    template_name = "assignments/delete_problem.html"
    success_url = "/problems/"
