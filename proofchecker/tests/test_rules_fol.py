from django.test import TestCase
from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj
from proofchecker.rules.existentialintro import ExistentialIntro
from proofchecker.rules.universalelim import UniversalElim
from proofchecker.utils import folparser


class FOLLexerTests(TestCase):

    def test_universal_elim(self):
        rule = UniversalElim()
        parser = folparser.parser

        # Test with valid input
        line1 = ProofLineObj('1', '∀x∈S H(x)', 'Premise')
        line2 = ProofLineObj('2', 'H(a)', '∀E 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertTrue(result.is_valid)
        self.assertEquals(result.err_msg, None)

        # Test where root operand of line 1 is not ∀
        line1 = ProofLineObj('1', '∃x∈S H(x)', 'Premise')
        line2 = ProofLineObj('2', 'H(a)', '∀E 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'The root operand of line 1 should be the universal quantifier (∀)')

        # Test where line 1 and line 2 refer to different predicates
        line1 = ProofLineObj('1', '∀x∈S H(x)', 'Premise')
        line2 = ProofLineObj('2', 'G(a)', '∀E 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'Lines 1 and 2 should refer to the same predicate')

        # Test where line 1 and 2 have different number of inputs
        line1 = ProofLineObj('1', '∀x∈S H(x, y)', 'Premise')
        line2 = ProofLineObj('2', 'H(a)', '∀E 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'The predicates on lines 1 and 2 do not have the same number of inputs')



    def test_universal_elim(self):
        rule = ExistentialIntro()
        parser = folparser.parser

        # Test with valid input
        line1 = ProofLineObj('1', 'H(a)', 'Premise')
        line2 = ProofLineObj('2', '∃x∈S H(x)', '∃I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertTrue(result.is_valid)
        self.assertEquals(result.err_msg, None)

        # Test where root operand of line 2 is not ∃
        line1 = ProofLineObj('1', 'H(a)', 'Premise')
        line2 = ProofLineObj('2', '∀x∈S H(x)', '∃I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'The root operand of line 1 should be the existential quantifier (∃)')

        # Test where line 1 and line 2 refer to different predicates
        line1 = ProofLineObj('1', 'G(a)', 'Premise')
        line2 = ProofLineObj('2', '∃x∈S H(x)', '∃I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'Lines 1 and 2 should refer to the same predicate')