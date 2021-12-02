from django.test import TestCase
from django.urls import reverse

from proofchecker.models import Proof, User

class ProofCheckerViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/proofs/checker/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('proof_checker'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('proof_checker'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proofchecker/proof_checker.html')

class ProofCreateViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/proofs/new/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('add_proof'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('add_proof'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proofchecker/proof_add_edit.html')

class ProofViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 5 proofs
        number_of_proofs = 13
        user = User()
        user.save()

        for proof_id in range(number_of_proofs):
            Proof.objects.create(
                premises = 'AvB',
                conclusion = '∧',
                created_by = user
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/proofs/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('all_proofs'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('all_proofs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proofchecker/allproofs.html')

    def test_lists_all_proofs(self):
        response = self.client.get(reverse('all_proofs'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['proof_list']), 13)
