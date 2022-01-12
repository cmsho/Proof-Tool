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

        # Test with proper input
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)

        # Test with invalid conjunction
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'C', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "The conjunction of lines 1 and 2 does not equal line 3")

        # Test with invalid line specification
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "Line numbers are not specified correctly.  Conjunction Introduction: ∧I m, n")    
    
    def test_conjunction_elim(self):
        rule = ConjunctionElim()

        # Test with proper input
        line1 = ProofLineObj('1', 'A∧B', 'Premise')
        line2 = ProofLineObj('2', 'A', '∧E 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertTrue(result.is_valid)

        line1 = ProofLineObj('1', '(A∧C)∨(B∧C)', 'Premise')
        line2 = ProofLineObj('2.1', 'A∧C', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', '∧E 2.1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid) 

        # Test with invalid conclusion
        line1 = ProofLineObj('1', 'A∧B', 'Premise')
        line2 = ProofLineObj('2', 'C', '∧E 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "Line 2 does not follow from line 1")

    def test_disjunction_intro(self):
        rule = DisjunctionIntro()

        # Test with valid input
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'A∨B', '∨I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertTrue(result.is_valid)

        # Test with invalid conclusion
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B∨C', '∨I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "Line 2 does not follow from line 1")

        # Test with invalid line citation
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'A∨B', '∨I 3')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertFalse(result.is_valid)


    def test_disjunction_elim(self): 
        rule = DisjunctionElim()

        # Test with valid input
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

        # Test with unequivalent expressions
        line1 = ProofLineObj('1', 'A∨B', 'Premise')
        line2 = ProofLineObj('2.1', 'A', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', 'Assumption')
        line4 = ProofLineObj('3.1', 'B', 'Assumption')
        line5 = ProofLineObj('3.2', 'D', 'Assumption')
        line6 = ProofLineObj('4', 'C', '∨E 1, 2, 3')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = rule.verify(line6, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "The expressions on lines 2.2, 3.2 and 4 are not equivalent")

        # Test with improper disjunction
        line1 = ProofLineObj('1', 'A∨B', 'Premise')
        line2 = ProofLineObj('2.1', 'A', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', 'Assumption')
        line4 = ProofLineObj('3.1', 'D', 'Assumption')
        line5 = ProofLineObj('3.2', 'C', 'Assumption')
        line6 = ProofLineObj('4', 'C', '∨E 1, 2, 3')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = rule.verify(line6, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "The expression on line 3.1 is not part of the disjunction on line 1")

        # Test with improper disjunction
        line1 = ProofLineObj('1', 'A∨B', 'Premise')
        line2 = ProofLineObj('2.1', 'D', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', 'Assumption')
        line4 = ProofLineObj('3.1', 'B', 'Assumption')
        line5 = ProofLineObj('3.2', 'C', 'Assumption')
        line6 = ProofLineObj('4', 'C', '∨E 1, 2, 3')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = rule.verify(line6, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "The expression on line 2.1 is not part of the disjunction on line 1")

        # Test with only one half of disjunction
        line1 = ProofLineObj('1', 'A∨B', 'Premise')
        line2 = ProofLineObj('2.1', 'A', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', 'Assumption')
        line4 = ProofLineObj('3.1', 'A', 'Assumption')
        line5 = ProofLineObj('3.2', 'C', 'Assumption')
        line6 = ProofLineObj('4', 'C', '∨E 1, 2, 3')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = rule.verify(line6, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "The expressions on lines 2.1 and 3.1 should be different")


    def test_negation_intro(self):
        rule = NegationIntro()

        # Test with valid input
        line1 = ProofLineObj('1.1', 'A', 'Premise')
        line2 = ProofLineObj('1.2', '⊥', 'Premise')
        line3 = ProofLineObj('2', '¬A', '¬I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)

        # Test without contradiction
        line1 = ProofLineObj('1.1', 'A', 'Premise')
        line2 = ProofLineObj('1.2', 'B', 'Premise')
        line3 = ProofLineObj('2', '¬A', '¬I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)   
        self.assertEqual(result.err_msg, "Line 1.2 should be '⊥' (Contradiction)")

        # Test without proper negation
        line1 = ProofLineObj('1.1', 'A', 'Premise')
        line2 = ProofLineObj('1.2', '⊥', 'Premise')
        line3 = ProofLineObj('2', '¬B', '¬I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)   
        self.assertEqual(result.err_msg, "Line 2 is not the negation of line 1.1")


    def test_negation_elim(self):
        rule = NegationElim()

        # Test with valid input
        line1 = ProofLineObj('1', '¬A', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', '⊥', '¬E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)

        # Test without contradiction
        line1 = ProofLineObj('1', '¬A', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', 'B', '¬E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "Line 3 should be '⊥' (Contradiction)")

        # Test without proper contradiction
        line1 = ProofLineObj('1', '¬A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', '⊥', '¬E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "Line 1 is not the negation of line 2")

        # Test with improper line specification
        line1 = ProofLineObj('1', '¬A', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', '⊥', '¬E 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "Line numbers are not specified correctly.  Negation Elimination: ¬E m, n")


    def test_conditional_intro(self):
        rule = ConditionalIntro()
        
        # Test with valid input
        line1 = ProofLineObj('1.1', 'A∧B', 'Premise')
        line2 = ProofLineObj('1.2', 'B', '∧E 1.1')
        line3 = ProofLineObj('2', '(A∧B)→B', '→I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)

        # Test with invalid input
        line1 = ProofLineObj('1.1', 'A∧B', 'Premise')
        line2 = ProofLineObj('1.2', 'B', '∧E 1.1')
        line3 = ProofLineObj('2', '(A∧B)→C', '→I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'The expressions on lines 1.1 and 1.2 do not match the implication on line 2')

        # Test with invalid citation
        line1 = ProofLineObj('1.1', 'A∧B', 'Premise')
        line2 = ProofLineObj('1.2', 'B', '∧E 1.1')
        line3 = ProofLineObj('2', '(A∧B)→B', '→I 3')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)


    def test_conditional_elim(self):
        rule = ConditionalElim()

        # Test with valid input
        line1 = ProofLineObj('1', 'A→B', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', 'B', '→E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)

        # Test with invalid elimination
        line1 = ProofLineObj('1', 'A→B', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', 'C', '→E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'The expressions on lines 2 and 3 do not match the implication on line 1')

        # Test with improper line specification
        line1 = ProofLineObj('1', 'A→B', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', 'B', '→E 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'Line numbers are not specified correctly.  Conditional Elimination (Modus Ponens): →E m, n')


    def test_biconditional_intro(self):
        rule = BiconditionalIntro()

        # Test with valid input
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

        # Test with valid input (all equiv)
        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'A', 'Assumption')
        line3 = ProofLineObj('2.1', 'A', 'Assumption')
        line4 = ProofLineObj('2.2', 'A', 'Assumption')
        line5 = ProofLineObj('3', 'A↔A', '↔I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5])
        result = rule.verify(line5, proof)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, None)

        # Test with unequivalent expressions
        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'C', 'Assumption')
        line3 = ProofLineObj('2.1', 'B', 'Assumption')
        line4 = ProofLineObj('2.2', 'A', 'Assumption')
        line5 = ProofLineObj('3', 'A↔B', '↔I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5])
        result = rule.verify(line5, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'The expressions on lines 1.2 and 2.1 are not equivalent')

        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'B', 'Assumption')
        line3 = ProofLineObj('2.1', 'B', 'Assumption')
        line4 = ProofLineObj('2.2', 'C', 'Assumption')
        line5 = ProofLineObj('3', 'A↔B', '↔I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5])
        result = rule.verify(line5, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'The expressions on lines 1.1 and 2.2 are not equivalent')

        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'B', 'Assumption')
        line3 = ProofLineObj('2.1', 'B', 'Assumption')
        line4 = ProofLineObj('2.2', 'A', 'Assumption')
        line5 = ProofLineObj('3', 'C↔B', '↔I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5])
        result = rule.verify(line5, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'Left side of line 3 does not equal either of the expressions on lines 1.2 and 2.2')

        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'B', 'Assumption')
        line3 = ProofLineObj('2.1', 'B', 'Assumption')
        line4 = ProofLineObj('2.2', 'A', 'Assumption')
        line5 = ProofLineObj('3', 'A↔C', '↔I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5])
        result = rule.verify(line5, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'Right side of line 3 does not equal either of the expressions on lines 1.2 and 2.2')

        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'A', 'Assumption')
        line3 = ProofLineObj('2.1', 'A', 'Assumption')
        line4 = ProofLineObj('2.2', 'A', 'Assumption')
        line5 = ProofLineObj('3', 'A↔B', '↔I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5])
        result = rule.verify(line5, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'Invalid introduction on line 3')

        # Test with invalid conclusion
        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'B', 'Assumption')
        line3 = ProofLineObj('2.1', 'B', 'Assumption')
        line4 = ProofLineObj('2.2', 'A', 'Assumption')
        line5 = ProofLineObj('3', 'A↔A', '↔I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5])
        result = rule.verify(line5, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, \
            'Left side and right side of line 3 are equiavlent, but lines 1.1 and 1.2 are not equivalent')


    def test_biconditional_elim(self):
        rule = BiconditionalElim()

        # Test with valid input
        line1 = ProofLineObj('1', 'A↔B', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'Assumption')
        line3 = ProofLineObj('3', 'B', '↔E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, None)

        line1 = ProofLineObj('1', 'A↔B', 'Assumption')
        line2 = ProofLineObj('2', 'B', 'Assumption')
        line3 = ProofLineObj('3', 'A', '↔E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, None)

        # Test with invalid input
        line1 = ProofLineObj('1', 'A↔B', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'Assumption')
        line3 = ProofLineObj('3', 'A', '↔E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "The expressions on lines 2 and 3 do not represent both the left and right side of the expression on line 1")

        # Test with invalid input
        line1 = ProofLineObj('1', 'A↔B', 'Assumption')
        line2 = ProofLineObj('2', 'C', 'Assumption')
        line3 = ProofLineObj('3', 'A', '↔E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "The expression on line 2 does not represent the left or right side of the expression on line 1")

        # Test with invalid input
        line1 = ProofLineObj('1', 'A↔B', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'Assumption')
        line3 = ProofLineObj('3', 'C', '↔E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "The expression on line 3 does not represent the left or right side of the expression on line 1")


    def test_indirect_proof(self):
        rule = IndirectProof()

        # Test with valid input
        line1 = ProofLineObj('1.1', '¬A', 'Premise')
        line2 = ProofLineObj('1.2', '⊥', 'X')
        line3 = ProofLineObj('2', 'A', 'IP 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertTrue(result.is_valid)

        # Test without contradition
        line1 = ProofLineObj('1.1', '¬A', 'Premise')
        line2 = ProofLineObj('1.2', 'B', 'Premise')
        line3 = ProofLineObj('2', 'A', 'IP 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "Line 1.2 should be '⊥' (Contradiction)")

        # Test with improper negation
        line1 = ProofLineObj('1.1', '¬A', 'Premise')
        line2 = ProofLineObj('1.2', '⊥', 'Premise')
        line3 = ProofLineObj('2', 'B', 'IP 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = rule.verify(line3, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "Line 1.1 is not the negation of line 2")


    def test_double_negation_elim(self):
        rule = DoubleNegationElim()

        # Test with valid input
        line1 = ProofLineObj('1', '¬¬A', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'DNE 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, None)

        # Test with invalid input
        line1 = ProofLineObj('1', '¬¬A', 'Assumption')
        line2 = ProofLineObj('2', 'B', 'DNE 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'Lines 1 and 2 are not equivalent')

        # Test with invalid input
        line1 = ProofLineObj('1', '¬A', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'DNE 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'Line 1 is not an instance of double-not operators')

        # Test with invalid input
        line1 = ProofLineObj('1', 'A^B', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'DNE 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "The main logical operator on line 1 is not '¬'")


    def test_explosion(self):
        rule = Explosion()

        # Test with proper input
        line1 = ProofLineObj('1', '⊥', 'Premise')
        line2 = ProofLineObj('2', 'B', 'X 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertTrue(result.is_valid)

        # Test without contradiction
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'X 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "Line 1 should be '⊥' (Contradiction)")

        # Test with invalid line citation
        line1 = ProofLineObj('1', '⊥', 'Premise')
        line2 = ProofLineObj('2', 'B', 'X 3')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertFalse(result.is_valid)


    def test_reiteration(self):
        rule = Reiteration()

        # Test with proper input
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'A', 'R 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertTrue(result.is_valid)

        # Test with unequivalent expressions
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'R 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'Lines 1 and 2 are not equivalent')

        # Test with invalid line citation
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'A', 'R 3')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = rule.verify(line2, proof)
        self.assertFalse(result.is_valid)