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

        # Test with valid input
        line1 = ProofLineObj('1', '∀x∈S H(x)', 'Premise')
        line2 = ProofLineObj('2', 'H(y)', '∀E 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'Instances of variable x on line 1 should be replaced with a name on line 2')

        # Test with valid input
        line1 = ProofLineObj('1', '∀x∈S H(x, x)', 'Premise')
        line2 = ProofLineObj('2', 'H(a, b)', '∀E 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'All instances of variable x on line 1 should be replaced with the same name on line 2')


    def test_existential_intro(self):
        rule = ExistentialIntro()
        parser = folparser.parser

        # Test with valid input
        line1 = ProofLineObj('1', 'H(a)', 'Premise')
        line2 = ProofLineObj('2', '∃x∈S H(x)', '∃I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertTrue(result.is_valid)
        self.assertEquals(result.err_msg, None)

        # Test with valid input
        line1 = ProofLineObj('1', 'H(a, a)', 'Premise')
        line2 = ProofLineObj('2', '∃x∈S H(x,a)', '∃I 1')
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

        # Test where line 1 and 2 have different number of inputs
        line1 = ProofLineObj('1', 'H(a, b)', 'Premise')
        line2 = ProofLineObj('2', '∃x∈S H(x)', '∃I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'The predicates on lines 1 and 2 do not have the same number of inputs')

        # Test where the variable on line 2 does not replace a name on line 1
        line1 = ProofLineObj('1', 'H(y)', 'Premise')
        line2 = ProofLineObj('2', '∃x∈S H(x)', '∃I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'Instances of variable x on line 2 should be represent a name on line 1')

        # Test where teh variables on line 2 replace two different names on line 1
        line1 = ProofLineObj('1', 'H(a, b)', 'Premise')
        line2 = ProofLineObj('2', '∃x∈S H(x, x)', '∃I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'All instances of variable x on line 2 should be represent the same name on line 1')