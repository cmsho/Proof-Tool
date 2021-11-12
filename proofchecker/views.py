from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.forms.models import modelformset_factory
from .forms import ProofForm, ProofLineForm, AssignmentForm
from .models import Proof, Problem, Assignment, Instructor, ProofLine
from .json_to_object import ProofTemp
from .proof import ProofObj, ProofLineObj, verify_proof, find_premises


# Create your views here.
def home(request):
    proofs = Proof.objects.all()
    context = {"proofs": proofs}
    return render(request, "proofchecker/home.html", context)


def AssignmentPage(request):
    return render(request, "proofchecker/assignment_page.html")

def ProofChecker(request):
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

# class HomeView(TemplateView):
#     template_name = "proofchecker/home.html"
#
#     def get_context_data(self):
#         context = super().get_context_data()
#         context["proofs"] = Proof.objects.all()
#         return context


class ProofView(ListView):
    model = Proof
    template_name = "proofchecker/allproofs.html"


class ProofDetailView(DetailView):
    model = Proof


def proof_create_view(request):
    ProofLineFormset = modelformset_factory(ProofLine, form=ProofLineForm, extra=0)
    qs = ProofLine.objects.none()
    form = ProofForm(request.POST or None)
    formset = ProofLineFormset(request.POST or None, queryset=qs)
    response_text = None

    if all([form.is_valid(), formset.is_valid()]):
        if 'check_proof' in request.POST:
            print("check_proof clicked")
            proof = ProofObj(lines=[])
            parent = form.save(commit=False)
            proof.premises = find_premises(parent.premises)
            print('\nPREMISES: ' + str(proof.premises))
            proof.conclusion = str(parent.conclusion)
            print('CONCLUSION: ' + proof.conclusion + '\n')
            for line in formset:
                proofline = ProofLineObj()
                child = line.save(commit=False)
                child.proof = parent
                proofline.line_no = str(child.line_no)
                print('LINE #: ' + proofline.line_no)
                proofline.expression = str(child.formula)
                print('\t EXPRESSION: ' + proofline.expression)
                proofline.rule = str(child.rule)
                print('\t RULE: ' + proofline.rule)
                proof.lines.append(proofline)
            # Verify the proof!
            response = verify_proof(proof)
            if response.is_valid:
                response_text = "validation successful!"
            else:
                response_text = response.err_msg
            print("\nPROOF.IS_VALID: " + str(response.is_valid))
            print("ERROR MESSAGE: " + str(response.err_msg))
        elif 'submit' in request.POST:
            parent = form.save(commit=False)
            parent.created_by = request.user
            parent.save()
            for f in formset:
                child = f.save(commit=False)
                child.proof = parent
                child.save()
            response_text = "proof added successfully!"

    context = {
        "form": form,
        "formset": formset,
        "response": response_text
    }

    return render(request, 'proofchecker/proof_add_edit.html', context)


def proof_update_view(request, pk=None):
    obj = get_object_or_404(Proof, pk=pk, created_by=request.user)
    qs = obj.proofline_set.all()

    form = ProofForm(request.POST or None, instance=obj)
    ProofLineFormset = modelformset_factory(ProofLine, form=ProofLineForm, extra=0)
    formset = ProofLineFormset(request.POST or None, queryset=qs)
    response_text = None

    if all([form.is_valid(), formset.is_valid()]):
        if 'check_proof' in request.POST:
            print("check_proof clicked")
            proof = ProofObj(lines=[])
            parent = form.save(commit=False)
            proof.premises = find_premises(parent.premises)
            print('\nPREMISES: ' + str(proof.premises))
            proof.conclusion = str(parent.conclusion)
            print('CONCLUSION: ' + proof.conclusion + '\n')
            for line in formset:
                proofline = ProofLineObj()
                child = line.save(commit=False)
                child.proof = parent
                proofline.line_no = str(child.line_no)
                print('LINE #: ' + proofline.line_no)
                proofline.expression = str(child.formula)
                print('\t EXPRESSION: ' + proofline.expression)
                proofline.rule = str(child.rule)
                print('\t RULE: ' + proofline.rule)
                proof.lines.append(proofline)
            # Verify the proof!
            response = verify_proof(proof)
            if response.is_valid:
                response_text = "validation successful!"
            else:
                response_text = response.err_msg
            print("\nPROOF.IS_VALID: " + str(response.is_valid))
            print("ERROR MESSAGE: " + str(response.err_msg))
        elif 'submit' in request.POST:
            print("submit button clicked")
            parent = form.save(commit=False)
            parent.save()
            for f in formset:
                child = f.save(commit=False)
                child.proof = parent
                child.save()
            response_text = "proof saved successfully!"

    context = {
        "form": form,
        "formset": formset,
        "object": obj,
        "response": response_text
    }

    return render(request, 'proofchecker/proof_add_edit.html', context)


def proof_create_view_temp(request):
    if request.method == 'POST':
        # new_premise = request.POST.get('premise')
        # new_conclusion = request.POST.get('conclusion')
        # new_proof_text = request.POST.get('proof_text')
        # new_proof = Proof.objects.create(premise=new_premise, conclusion=new_conclusion,
        #                                  created_by=request.user)
        # new_proof.save()

        req_body = '''{
                                    "premises": ["A", "B"],
                                    "conclusion": "A∧B",
                                    "lines": [{
                                            "line_no": "1",
                                            "expression": "A",
                                            "rule": "Premise"
                                        },
                                        {
                                            "line_no": "2",
                                            "expression": "B",
                                            "rule": "Premise"
                                        },
                                        {
                                            "line_no": "3",
                                            "expression": "A∧B",
                                            "rule": "∧I 1, 2"
                                        }
                                    ]
                            }'''
        jsonProof = ProofTemp.from_json(req_body)

        modelProof = Proof.objects.create(premises=jsonProof.premises, conclusion=jsonProof.conclusion,
                                          created_by=request.user)
        modelProof.save()

        for line in jsonProof.lines:
            print(line)
            modelLine = ProofLine.objects.create(proof_id=modelProof.id, line_no=line['line_no'],
                                                 formula=line['expression'], rule=line['rule'])
            modelLine.save()

        print(jsonProof.premises)

    return render(request, 'proofchecker/proof_add_edit.html')


# class ProofCreateView(CreateView):
#     model = Proof
#     template_name = "proofchecker/proof_add_edit.html"
#     form_class = ProofForm
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)
#
#
# class ProofUpdateView(UpdateView):
#     model = Proof
#     template_name = "proofchecker/proof_add_edit.html"
#     form_class = ProofForm


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
