from django.test import TestCase

from proofchecker.proof import ProofObj, ProofLineObj
from proofchecker.rules.assumption import Assumption
from proofchecker.rules.biconditionalelim import BiconditionalElim
from proofchecker.rules.biconditionalintro import BiconditionalIntro
from proofchecker.rules.conditionalelim import ConditionalElim
from proofchecker.rules.conditionalintro import ConditionalIntro
from proofchecker.rules.conjunctionintro import ConjunctionIntro
from proofchecker.rules.conjunctionelim import ConjunctionElim
from proofchecker.rules.disjunctionintro import DisjunctionIntro
from proofchecker.rules.disjunctionelim import DisjunctionElim
from proofchecker.rules.doublenegationelim import DoubleNegationElim
from proofchecker.rules.explosion import Explosion
from proofchecker.rules.indirectproof import IndirectProof
from proofchecker.rules.negationelim import NegationElim
from proofchecker.rules.negationintro import NegationIntro
from proofchecker.rules.premise import Premise
from proofchecker.rules.reiteration import Reiteration


class RuleTests(TestCase):

    def test_premise(self):
        """
        Test that the function verify_premise is working properly
        """
        # Test with proper input
        rule = Premise()
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(premises=['A', 'B'], lines=[])
        proof.lines.extend([line1, line2, line3])
        result1 = rule.verify(line1, proof)
        result2 = rule.verify(line2, proof)
        self.assertTrue(result1.is_valid)
        self.assertTrue(result2.is_valid)
    
        # Test with a line not in premises    
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(premises='A', lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line2, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "Expression on line 2 is not a premise")

        # Test with a line not found in multiple premises input
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'C', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(premises=['A', 'B'], lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line2, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "Expression on line 2 not found in premises")

        # Test with an invalid premise    
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B∧', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(premises='A', lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line2, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "One or more premises is invalid")

    def test_assumption(self):
        """
        Test that the function verify_assumption is working properly
        """
        # Test with valid input
        rule = Assumption()
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2.1', 'B', 'Assumption')
        line3 = ProofLineObj('2.2', 'A∧B', '∧I 1, 2')
        proof = ProofObj(premises='A', lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line2, proof)
        self.assertTrue(result.is_valid)

        # Test with invalid input
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2.1', 'B', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', 'Assumption')
        proof = ProofObj(premises='A', lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'Assumptions can only exist at the start of a subproof')     

    def test_conjunction_intro(self):
        rule = ConjunctionIntro()
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)
    
    def test_conjunction_elim(self):
        rule = ConjunctionElim()
        line1 = ProofLineObj('1', 'A∧B', 'Premise')
        line2 = ProofLineObj('2', 'A', '∧E 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertTrue(result.is_valid)

    def test_disjunction_intro(self):
        rule = DisjunctionIntro()
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'A∨B', '∨I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertTrue(result.is_valid)

    def test_disjunction_elim(self): 
        rule = DisjunctionElim()
        line1 = ProofLineObj('1', 'A∨B', 'Premise')
        line2 = ProofLineObj('2.1', 'A', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', 'Assumption')
        line4 = ProofLineObj('3.1', 'B', 'Assumption')
        line5 = ProofLineObj('3.2', 'C', 'Assumption')
        line6 = ProofLineObj('4', 'C', '∨E 1, 2, 3')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = rule.verify(line6, proof)
        self.assertTrue(result.is_valid)

    def test_negation_intro(self):
        rule = NegationIntro()
        line1 = ProofLineObj('1.1', 'A', 'Premise')
        line2 = ProofLineObj('1.2', '⊥', 'Premise')
        line3 = ProofLineObj('2', '¬A', '¬I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)

    def test_negation_elim(self):
        rule = NegationElim()
        line1 = ProofLineObj('1', '¬A', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', '⊥', '¬E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)

    def test_conditional_intro(self):
        rule = ConditionalIntro()
        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'B', 'Assumption')
        line3 = ProofLineObj('2', 'A→B', '→I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)

    def test_conditional_elim(self):
        rule = ConditionalElim()
        line1 = ProofLineObj('1', 'A→B', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', 'B', '→E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)

    def test_biconditional_intro(self):
        rule = BiconditionalIntro()
        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'B', 'Assumption')
        line3 = ProofLineObj('2.1', 'B', 'Assumption')
        line4 = ProofLineObj('2.2', 'A', 'Assumption')
        line5 = ProofLineObj('3', 'A↔B', '↔I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5])
        result = rule.verify(line5, proof)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, None)

    def test_biconditional_elim(self):
        rule = BiconditionalElim()
        line1 = ProofLineObj('1', 'A↔B', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'Assumption')
        line3 = ProofLineObj('3', 'B', '↔E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, None)

    def test_indirect_proof(self):
        rule = IndirectProof()
        line1 = ProofLineObj('1.1', '¬A', 'Premise')
        line2 = ProofLineObj('1.2', '⊥', 'Premise')
        line3 = ProofLineObj('2', 'A', 'IP 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)

    def test_double_negation_elim(self):
        rule = DoubleNegationElim()
        line1 = ProofLineObj('1', '¬¬A', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'DNE 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, None)

    def test_explosion(self):
        rule = Explosion()
        line1 = ProofLineObj('1', '⊥', 'Premise')
        line2 = ProofLineObj('2', 'B', 'X 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertTrue(result.is_valid)

    def test_reiteration(self):
        rule = Reiteration()
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'A', 'R 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertTrue(result.is_valid)