from django.test import TestCase
from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj
from proofchecker.rules.existentialelim import ExistentialElim
from proofchecker.rules.existentialintro import ExistentialIntro
from proofchecker.rules.universalelim import UniversalElim
from proofchecker.rules.universalintro import UniversalIntro
from proofchecker.utils import folparser


class FOLRulesTests(TestCase):

    def test_existential_intro(self):
        rule = ExistentialIntro()
        parser = folparser.parser

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

        # Test where the variables on line 2 replace two different names on line 1
        line1 = ProofLineObj('1', 'H(a, b)', 'Premise')
        line2 = ProofLineObj('2', '∃x∈S H(x, x)', '∃I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'All instances of variable x on line 2 should be represent the same name on line 1')

        # Test where the variable on line 2 already appears on line 1
        line1 = ProofLineObj('1', 'H(a, x)', 'Premise')
        line2 = ProofLineObj('2', '∃x∈S H(x, x)', '∃I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'Variable x on line 2 should not appear on line 1')

    def test_existential_elim(self):
        rule = ExistentialElim()
        parser = folparser.parser

        # Test with valid input
        line1 = ProofLineObj('1', '∃x∈S F(x, x)', 'Premise')
        line2 = ProofLineObj('2.1', 'F(a, a)', 'Assumption')
        line3 = ProofLineObj('2.2', 'F(a, a)', 'R 2.1')
        line4 = ProofLineObj('3', 'F(a, a)', '∃E 1, 2')
        proof = ProofObj(lines=[line1, line2, line3, line4])
        result = rule.verify(line4, proof, parser)
        self.assertTrue(result.is_valid)
        self.assertEquals(result.err_msg, None)

        # Test where the root operand of line 1 is not ∃ 
        line1 = ProofLineObj('1', '∀x∈S F(x, x)', 'Premise')
        line2 = ProofLineObj('2.1', 'F(a, a)', 'Assumption')
        line3 = ProofLineObj('2.2', 'F(a, a)', 'R 2.1')
        line4 = ProofLineObj('3', 'F(a, a)', '∃E 1, 2')
        proof = ProofObj(lines=[line1, line2, line3, line4])
        result = rule.verify(line4, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'The root operand of line 1 should be the existential quantifier (∃)')

        # Test where lines 1 and 2.1 refer to different predicates
        line1 = ProofLineObj('1', '∃x∈S G(x, x)', 'Premise')
        line2 = ProofLineObj('2.1', 'F(a, a)', 'Assumption')
        line3 = ProofLineObj('2.2', 'F(a, a)', 'R 2.1')
        line4 = ProofLineObj('3', 'F(a, a)', '∃E 1, 2')
        proof = ProofObj(lines=[line1, line2, line3, line4])
        result = rule.verify(line4, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'Lines 1 and 2.1 should refer to the same predicate')

        # Test where lines 1 and 2.1 have different numbers of inputs
        line1 = ProofLineObj('1', '∃x∈S F(x, x)', 'Premise')
        line2 = ProofLineObj('2.1', 'F(a)', 'Assumption')
        line3 = ProofLineObj('2.2', 'F(a)', 'R 2.1')
        line4 = ProofLineObj('3', 'F(a)', '∃E 1, 2')
        proof = ProofObj(lines=[line1, line2, line3, line4])
        result = rule.verify(line4, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'The predicates on lines 1 and 2.1 do not have the same number of inputs')

        # Test where instances of bound var on line 1 are replaced by another var
        line1 = ProofLineObj('1', '∃x∈S F(x, x)', 'Premise')
        line2 = ProofLineObj('2.1', 'F(y, y)', 'Assumption')
        line3 = ProofLineObj('2.2', 'F(y, y)', 'R 2.1')
        line4 = ProofLineObj('3', 'F(y, y)', '∃E 1, 2')
        proof = ProofObj(lines=[line1, line2, line3, line4])
        result = rule.verify(line4, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'Instances of variable x on line 1 should be replaced with a name on line 2.1')

        # Test where bound var on line 1 is replaced by different names on line 2.1
        line1 = ProofLineObj('1', '∃x∈S F(x, x)', 'Premise')
        line2 = ProofLineObj('2.1', 'F(a, b)', 'Assumption')
        line3 = ProofLineObj('2.2', 'F(a, b)', 'R 2.1')
        line4 = ProofLineObj('3', 'F(a, b)', '∃E 1, 2')
        proof = ProofObj(lines=[line1, line2, line3, line4])
        result = rule.verify(line4, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'All instances of variable x on line 1 should be replaced with the same name on line 2.1')

        # Test where line i_x and current line have different expressions
        line1 = ProofLineObj('1', '∃x∈S F(x, x)', 'Premise')
        line2 = ProofLineObj('2.1', 'F(a, a)', 'Assumption')
        line3 = ProofLineObj('2.2', 'F(a, a)', 'R 2.1')
        line4 = ProofLineObj('3', 'F(b, b)', '∃E 1, 2')
        proof = ProofObj(lines=[line1, line2, line3, line4])
        result = rule.verify(line4, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'The expressions on line 2.2 and line 3 should be equivalent')


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


    def test_universal_intro(self):
        rule = UniversalIntro()
        parser = folparser.parser

        # Test with valid input
        line1 = ProofLineObj('1', 'H(a, a, b)', 'Premise')
        line2 = ProofLineObj('2', '∀x∈S H(x, x, b)', '∀I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertTrue(result.is_valid)
        self.assertEquals(result.err_msg, None)

        # Test where root operand of line 2 is not ∀
        line1 = ProofLineObj('1', 'H(a)', 'Premise')
        line2 = ProofLineObj('2', '∃x∈S H(x)', '∀I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'The root operand of line 1 should be the universal quantifier (∀)')

        # Test where line 1 and line 2 refer to different predicates
        line1 = ProofLineObj('1', 'G(a)', 'Premise')
        line2 = ProofLineObj('2', '∀x∈S H(x)', '∀I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'Lines 1 and 2 should refer to the same predicate')

        # Test where line 1 and 2 have different number of inputs
        line1 = ProofLineObj('1', 'H(a, b)', 'Premise')
        line2 = ProofLineObj('2', '∀x∈S H(x)', '∀I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'The predicates on lines 1 and 2 do not have the same number of inputs')

        # Test where the variable on line 2 does not replace a name on line 1
        line1 = ProofLineObj('1', 'H(y)', 'Premise')
        line2 = ProofLineObj('2', '∀x∈S H(x)', '∀I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'Instances of variable x on line 2 should be represent a name on line 1')

        # Test where the variables on line 2 replace two different names on line 1
        line1 = ProofLineObj('1', 'H(a, b)', 'Premise')
        line2 = ProofLineObj('2', '∀x∈S H(x, x)', '∀I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'All instances of variable x on line 2 should be represent the same name on line 1')

        # Test where the variable on line 2 already appears on line 1
        line1 = ProofLineObj('1', 'H(a, x)', 'Premise')
        line2 = ProofLineObj('2', '∀x∈S H(x, x)', '∀I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'Variable x on line 2 should not appear on line 1')

        # Test where the variable on line 2 already appears on line 1
        line1 = ProofLineObj('1', 'H(a, a, b)', 'Premise')
        line2 = ProofLineObj('2', '∀x∈S H(x, y, b)', '∀I 1')
        proof = ProofObj(lines=[line1, line2])
        result = rule.verify(line2, proof, parser)
        # self.assertFalse(result.is_valid)
        self.assertEquals(result.err_msg, 'All instances of name a on line 1 should be replaced with the bound variable x on line 2')