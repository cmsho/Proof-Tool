from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory
from .forms import ProofForm, ProofLineForm, AssignmentForm
from .models import Proof, Problem, Assignment, Instructor, ProofLine
from .json_to_object import ProofTemp
from .proof import ProofObj, ProofLineObj, verify_proof, find_premises


def home(request):
    proofs = Proof.objects.all()
    context = {"proofs": proofs}
    return render(request, "proofchecker/home.html", context)


def AssignmentPage(request):
    return render(request, "proofchecker/assignment_page.html")


def single_proof_checker(request):
    ProofLineFormset = modelformset_factory(ProofLine, form=ProofLineForm, extra=0)
    qs = ProofLine.objects.none()
    form = ProofForm(request.POST or None)
    formset = ProofLineFormset(request.POST or None, queryset=qs)

    if all([form.is_valid(), formset.is_valid()]):
        
        # Create a new proof object
        proof = ProofObj(lines=[])

        # Grab premise and conclusion from the form
        # Assign them to the proof object
        parent = form.save(commit=False)
        proof.premises = find_premises(parent.premises)
        print('\nPREMISES: ' + str(proof.premises))
        proof.conclusion = str(parent.conclusion)
        print('CONCLUSION: ' + proof.conclusion + '\n')

        for line in formset:
            # Create a proofline object
            proofline = ProofLineObj()

            # Grab the line_no, formula, and expression from the form
            # Assign them to the proofline object
            child = line.save(commit=False)
            child.proof = parent
            
            proofline.line_no = str(child.line_no)
            print('LINE #: ' + proofline.line_no)
            proofline.expression = str(child.formula)
            print('\t EXPRESSION: ' + proofline.expression)
            proofline.rule = str(child.rule)
            print('\t RULE: ' + proofline.rule)

            # Append the proofline to the proof object's lines
            proof.lines.append(proofline)

        # Verify the proof!
        response = verify_proof(proof)
        print("\nPROOF.IS_VALID: " + str(response.is_valid))
        print("ERROR MESSAGE: " + str(response.err_msg))

        # Send the response back
        context = {
            "form": form,
            "formset": formset,
            "response": response
        }

        return render(request, 'proofchecker/single_proof_checker.html', context)

    context = {
        "form": form,
        "formset": formset
    }
    return render(request, 'proofchecker/single_proof_checker.html', context)


def proof_checker(request):
    ProofLineFormset = modelformset_factory(ProofLine, form=ProofLineForm, extra=0)
    qs = ProofLine.objects.none()
    form = ProofForm(request.POST or None)
    formset = ProofLineFormset(request.POST or None, queryset=qs)

    if all([form.is_valid(), formset.is_valid()]):
        
        # Create a new proof object
        proof = ProofObj(lines=[])

        # Grab premise and conclusion from the form
        # Assign them to the proof object
        parent = form.save(commit=False)
        proof.premises = find_premises(parent.premises)
        print('\nPREMISES: ' + str(proof.premises))
        proof.conclusion = str(parent.conclusion)
        print('CONCLUSION: ' + proof.conclusion + '\n')

        for line in formset:
            # Create a proofline object
            proofline = ProofLineObj()

            # Grab the line_no, formula, and expression from the form
            # Assign them to the proofline object
            child = line.save(commit=False)
            child.proof = parent
            
            proofline.line_no = str(child.line_no)
            print('LINE #: ' + proofline.line_no)
            proofline.expression = str(child.formula)
            print('\t EXPRESSION: ' + proofline.expression)
            proofline.rule = str(child.rule)
            print('\t RULE: ' + proofline.rule)

            # Append the proofline to the proof object's lines
            proof.lines.append(proofline)

        # Verify the proof!
        response = verify_proof(proof)
        print("\nPROOF.IS_VALID: " + str(response.is_valid))
        print("ERROR MESSAGE: " + str(response.err_msg))

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








def proof_create_view(request):
    ProofLineFormset = modelformset_factory(ProofLine, form=ProofLineForm, extra=0, can_delete=True)
    query_set = ProofLine.objects.none()
    form = ProofForm(request.POST or None)
    formset = ProofLineFormset(request.POST or None, queryset=query_set)
    response = None

    if request.POST:
        if all([form.is_valid(), formset.is_valid()]):
            parent = form.save(commit=False)
            if 'check_proof' in request.POST:
                proof = ProofObj(lines=[]) #
                proof.premises = find_premises(parent.premises)
                proof.conclusion = str(parent.conclusion)

                for line in formset:
                    if len(line.cleaned_data) > 0 and not line.cleaned_data['DELETE']:
                        proofline = ProofLineObj()
                        child = line.save(commit=False)
                        child.proof = parent
                        proofline.line_no = str(child.line_no)
                        proofline.expression = str(child.formula)
                        proofline.rule = str(child.rule)
                        proof.lines.append(proofline)

                response = verify_proof(proof)

            elif 'submit' in request.POST:
                parent.created_by = request.user
                parent.save()
                for line in formset:
                    if len(line.cleaned_data) > 0 and not line.cleaned_data['DELETE']:
                        child = line.save(commit=False)
                        child.proof = parent
                        child.save()

                return HttpResponseRedirect(reverse('all_proofs'))
    context = {
        "form": form,
        "formset": formset,
        "response": response
    }
    return render(request, 'proofchecker/proof_add_edit.html', context)







def proof_update_view(request, pk=None):
    obj = get_object_or_404(Proof, pk=pk)
    ProofLineFormset = modelformset_factory(ProofLine, form=ProofLineForm, extra=0, can_delete=True)
    query_set = obj.proofline_set.all()
    form = ProofForm(request.POST or None, instance=obj)
    formset = ProofLineFormset(request.POST or None, queryset=query_set)
    response = None

    if request.POST:
        parent = form.save(commit=False)
        if all([form.is_valid(), formset.is_valid()]):
            if 'check_proof' in request.POST:
                proof = ProofObj(lines=[]) #
                proof.premises = find_premises(parent.premises)
                proof.conclusion = str(parent.conclusion)

                for line in formset:
                    if len(line.cleaned_data) > 0 and not line.cleaned_data['DELETE']:
                        print("CLEANED_DATA: " + str(line.cleaned_data))
                        proofline = ProofLineObj()
                        child = line.save(commit=False)
                        child.proof = parent
                        proofline.line_no = str(child.line_no)
                        proofline.expression = str(child.formula)
                        proofline.rule = str(child.rule)
                        proof.lines.append(proofline)
                        
                response = verify_proof(proof)

            elif 'submit' in request.POST:
                parent.created_by = request.user
                parent.save()

                for line in formset:
                    print("CLEANED_DATA: " + str(line.cleaned_data))
                    if len(line.cleaned_data) > 0:
                        print(line.cleaned_data)
                        child = line.save(commit=False)
                        child.proof = parent
                        child.save()

                        if line.cleaned_data['DELETE']:
                            child.delete()

                return HttpResponseRedirect(reverse('all_proofs'))

    context = {
        "object": obj,
        "form": form,
        "formset": formset,
        "response": response
    }
    return render(request, 'proofchecker/proof_add_edit.html', context)


class ProofView(ListView):
    model = Proof
    template_name = "proofchecker/allproofs.html"


class ProofDetailView(DetailView):
    model = Proof

class ProofDeleteView(DeleteView):
    model = Proof
    template_name = "proofchecker/delete_proof.html"
    success_url = "/proofs/"


class ProblemView(ListView):
    model = Problem
    template_name = "proofchecker/problems.html"


class AssignmentView(ListView):
    model = Assignment
    template_name = "proofchecker/assignments.html"


class AssignmentCreateView(CreateView):
    model = Assignment
    template_name = "proofchecker/add_assignment.html"
    form_class = AssignmentForm

    def form_valid(self, form):
        form.instance.created_by = Instructor.objects.get(user=self.request.user)
        return super().form_valid(form)


class AssignmentUpdateView(UpdateView):
    model = Assignment
    template_name = "proofchecker/update_assignment.html"
    form_class = AssignmentForm


class AssignmentDeleteView(DeleteView):
    model = Assignment
    template_name = "proofchecker/delete_assignment.html"
    success_url = "/assignments/"
