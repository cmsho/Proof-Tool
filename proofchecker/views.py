from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ProofForm, ProofLineForm, AssignmentForm
from .models import Proof, Problem, Assignment, Instructor


# Create your views here.
def home(request):
    proofs = Proof.objects.all()
    context = {"proofs": proofs}
    return render(request, "proofchecker/home.html", context)


def AssignmentPage(request):
    return render(request, "proofchecker/assignment_page.html")


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
    form = ProofForm(request.POST or None)
    form_2 = ProofLineForm(request.POST or None)
    context = {
        "form": form,
        "form_2": form_2
    }

    if all([form.is_valid(), form_2.is_valid()]):
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, 'proofchecker/add_proof.html', context)


def proof_update_view(request, id=None):
    obj = get_object_or_404(Proof, id=id, user=request.user)
    form = ProofForm(request.POST or None, instance=obj)
    form_2 = ProofLineForm(request.POST or None)
    context = {
        "form": form,
        "form_2": form_2,
        "object": obj
    }

    # if all([form.is_valid(), form_2.is_valid()]):


# def proof_create_view(request):
#     if request.method == 'POST':
#         new_premise = request.POST.get('premise')
#         new_conclusion = request.POST.get('conclusion')
#         new_proof_text = request.POST.get('proof_text')
#         new_proof = Proof.objects.create(premise=new_premise, conclusion=new_conclusion,
#                                          created_by=request.user)
#         new_proof.save()
#     return render(request, 'proofchecker/add_proof1.html')


# class ProofCreateView(CreateView):
#     model = Proof
#     template_name = "proofchecker/add_proof.html"
#     form_class = ProofForm
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)


class ProofUpdateView(UpdateView):
    model = Proof
    template_name = "proofchecker/edit_proof.html"
    form_class = ProofForm


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
