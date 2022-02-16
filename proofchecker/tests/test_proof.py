from django.test import TestCase
from django.urls import reverse

from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj
from proofchecker.proofs.proofutils import get_line_no, get_line_nos, get_lines_in_subproof, \
    get_premises, is_conclusion, is_valid_expression, is_var, verify_expression, verify_line_citation, \
    depth, verify_line_citation, clean_rule
from proofchecker.proofs.proofchecker import verify_proof, verify_rule
from proofchecker.utils import tflparser


class ProofLineObjTests(TestCase):

    def test_proofline_construction(self):
        """
        Test that a ProofLine can be constructed appropriately
        """
        line1 = ProofLineObj('1', '(A∧C)∨(B∧C)', 'Premise')
        self.assertEqual('1', line1.line_no)
        self.assertEqual('(A∧C)∨(B∧C)', line1.expression)
        self.assertEqual('Premise', line1.rule)

    def test_proofline_obj_to_string(self):
        """
        Test that the ProofLineObj __str__ method works appropriately
        """
        line1 = ProofLineObj('1', 'A∨B', 'Premise')
        self.assertEqual(str(line1), 'Line 1: A∨B, Premise')

class ProofObjTests(TestCase):

    def test_proof_construction(self):
        """
        Test that a Proof can be constructed appropriately
        """
        line1 = ProofLineObj('1', '(A∧C)∨(B∧C)', 'Premise')
        line2_1 = ProofLineObj('2.1', '(A∧C)', 'Assumption')
        line2_2 = ProofLineObj('2.2', 'C', '∧E 2.1')
        line3_1 = ProofLineObj('3.1', '(B∧C)', 'Assumption')
        line3_2 = ProofLineObj('3.2', 'C', '∧E 2.1')
        line4 = ProofLineObj('4', 'C', '∨E, 1, 2, 3')
        proof = ProofObj(lines=[line1, line2_1, line2_2, line3_1, line3_2, line4])
        self.assertEqual(len(proof.lines), 6)

    def test_proof_obj_to_string(self):
        """
        Test that the ProofObj __str__ method works appropriately
        """
        line1 = ProofLineObj('1', 'A∧B', 'Premise')
        line2 = ProofLineObj('2', 'A', '∧E 1')
        str1 = "Line 1: A∧B, Premise\nLine 2: A, ∧E 1\n"
        proof = ProofObj(
            premises = "A∧B",
            conclusion = 'A',
            lines = [line1, line2]
        )
        self.assertEqual(str(proof), str1)

class GettersTests(TestCase):

    def test_get_line_no(self):
        """
        Test that the get_line_no method is working properly
        """
        rule1 = '¬I 2'
        rule2 = '∧E 3.1'
        rule3 = '∨I 4.12.3.5'
        self.assertEqual(get_line_no(rule1), '2')
        self.assertEqual(get_line_no(rule2), '3.1')
        self.assertEqual(get_line_no(rule3), '4.12.3.5')

    def test_get_line_nos(self):
        """
        Test that the get_line_nos method is working properly
        """
        rule1 = '∨E, 1, 2, 3'
        rule2 = '→I 2-3'
        self.assertEqual(get_line_nos(rule1), ['1', '2', '3'])
        self.assertEqual(get_line_nos(rule2), ['2', '3'])
    
    def test_get_lines_in_subproof_with_valid_subproof(self):
        """
        Test that the get_lines_in_subproof method is working properly
        """
        # Test with multi-line subproof
        line1 = ProofLineObj('1', '(A∧C)∨(B∧C)', 'Premise')
        line2_1 = ProofLineObj('2.1', '(A∧C)', 'Assumption')
        line2_2 = ProofLineObj('2.2', 'C', '∧E 2.1')
        proof = ProofObj(lines=[line1, line2_1, line2_2])
        result = get_lines_in_subproof('2', proof)
        self.assertEqual(result, [line2_1, line2_2])

        # Test with single-line subproof
        line1 = ProofLineObj('1', 'A∨(A∧B)', 'Premise')
        line2_1 = ProofLineObj('2.1', 'A', 'Assumption')
        line3_1 = ProofLineObj('3.1', 'A∧B', 'Assumption')
        line3_2 = ProofLineObj('3.2', 'A', '∧E 3.1')
        line4 = ProofLineObj('4', 'A', '∨E 1, 2, 3')
        proof = ProofObj(lines=[line1, line2_1, line3_1, line3_2, line4])
        result = get_lines_in_subproof('2', proof)
        self.assertEqual(result, [line2_1, line2_1])

    def test_get_lines_in_subproof_with_invalid_subproof(self):
        """
        Test that the get_lines_in_subproof method is working properly
        """
        line1 = ProofLineObj('1', '(A∧C)∨(B∧C)', 'Premise')
        line2_1 = ProofLineObj('2.1', '(A∧C)', 'Assumption')
        proof = ProofObj(lines=[line1, line2_1])
        result = get_lines_in_subproof('3', proof)
        self.assertEqual(result, None)
    
    def test_get_premises(self):
        """
        Test that the get_premises method is working properly
        """
        str1 = 'A∧C; B∧C; D; E'
        result = get_premises(str1)
        self.assertEqual(result, ['A∧C', 'B∧C', 'D', 'E'])

class HelpersTests(TestCase):

    def test_clean_rule(self):
        """
        Verify that the clean_rule function works appropriately
        """
        str1 = '&E 1'
        str2 = '^I 2'
        str3 = '~E 3'
        str4 = '-I 4'
        str5 = '>I 5'
        str6 = '->E 6'
        self.assertEqual(clean_rule(str1), '∧E 1')
        self.assertEqual(clean_rule(str2), '∧I 2')
        self.assertEqual(clean_rule(str3), '¬E 3')
        self.assertEqual(clean_rule(str4), '¬I 4')
        self.assertEqual(clean_rule(str5), '→I 5')
        self.assertEqual(clean_rule(str6), '→E 6')

    def test_depth(self):
        """
        Verify that the depth() function returns the correct depth
        """
        str1 = '3'
        str2 = '3.12.4'
        str3 = '3.12.4.66666.7.16.5'
        a = depth(str1)
        b = depth(str2)
        c = depth(str3)
        self.assertEqual(a, 1)
        self.assertEqual(b, 3)
        self.assertEqual(c, 7)

    def test_is_valid_expression(self):
        """
        Test that the is_valid_expression method works properly
        """
        parser=tflparser.parser
        str1 = "(A∧C)∨(B∧C)"
        str2 = "(A∧C)∨"
        str3 = ""
        self.assertTrue(is_valid_expression(str1, parser))
        self.assertFalse(is_valid_expression(str2, parser))
        self.assertFalse(is_valid_expression(str3, parser))

    def test_verify_expression(self):
        """
        Test that the verify_expression method works properly
        """
        parser = tflparser.parser
        str1 = "(A∧C)∨(B∧C)"
        str2 = "(A∧C)∨"
        str3 = ""
        str4 = "A!"
        res1 = verify_expression(str1, parser)
        res2 = verify_expression(str2, parser)
        res3 = verify_expression(str3, parser)
        res4 = verify_expression(str4, parser)
        self.assertTrue(res1.is_valid)
        self.assertFalse(res2.is_valid)
        self.assertEqual(res2.err_msg, "Syntax error in expression (A∧C)∨")
        self.assertFalse(res3.is_valid)
        self.assertEqual(res3.err_msg, "Expression cannot be an empty string")
        self.assertFalse(res4.is_valid)
        self.assertEqual(res4.err_msg, "Illegal character '!' in expression A!")

    def test_is_var(self):
        """
        Test that the is_var method properly determines 
        if a char is an FOL variable
        """
        self.assertTrue(is_var('s'))
        self.assertTrue(is_var('t'))
        self.assertTrue(is_var('y'))
        self.assertTrue(is_var('z'))

        self.assertFalse(is_var('a'))
        self.assertFalse(is_var('r'))
        self.assertFalse(is_var('1'))
        self.assertFalse(is_var('s, z'))
        


class ProofCheckerTests(TestCase):
    def test_verify_rule(self):
        """
        Test that the verify_rule function is working properly
        """
        # Test and_intro
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(lines=[line1, line2, line3])
        parser = tflparser.parser
        result = verify_rule(line3, proof, parser)
        self.assertTrue(result.is_valid)

        # Test and_elim
        line1 = ProofLineObj('1', 'A∧B', 'Premise')
        line2 = ProofLineObj('2', 'A', '∧E 1')
        proof = ProofObj(lines=[line1, line2])
        parser = tflparser.parser
        result = verify_rule(line2, proof, parser)
        self.assertTrue(result.is_valid)

        # Test or_intro
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'A∨B', '∨I 1')
        proof = ProofObj(lines=[line1, line2])
        parser = tflparser.parser
        result = verify_rule(line2, proof, parser)
        self.assertTrue(result.is_valid)

        # Test or_elim
        line1 = ProofLineObj('1', 'A∨B', 'Premise')
        line2 = ProofLineObj('2.1', 'A', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', 'Assumption')
        line4 = ProofLineObj('3.1', 'B', 'Assumption')
        line5 = ProofLineObj('3.2', 'C', 'Assumption')
        line6 = ProofLineObj('4', 'C', '∨E 1, 2, 3')
        proof = ProofObj(lines=[line1, line2, line3, line4, line5, line6])
        parser = tflparser.parser
        result = verify_rule(line6, proof, parser)
        self.assertTrue(result.is_valid)

        # Test not_intro
        line1 = ProofLineObj('1.1', 'A', 'Premise')
        line2 = ProofLineObj('1.2', '⊥', 'Premise')
        line3 = ProofLineObj('2', '¬A', '¬I 1')
        proof = ProofObj(lines=[line1, line2, line3])
        parser = tflparser.parser
        result = verify_rule(line3, proof, parser)
        self.assertTrue(result.is_valid)

        # Test not_elim
        line1 = ProofLineObj('1', '¬A', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', '⊥', '¬E 1, 2')
        proof = ProofObj(lines=[line1, line2, line3])
        parser = tflparser.parser
        result = verify_rule(line3, proof, parser)
        self.assertTrue(result.is_valid)

        # Test implies_intro
        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'B', 'Assumption')
        line3 = ProofLineObj('2', 'A→B', '→I 1')
        proof = ProofObj(lines=[line1, line2, line3])
        parser = tflparser.parser
        result = verify_rule(line3, proof, parser)
        self.assertTrue(result.is_valid)

        # Test implies_elim
        line1 = ProofLineObj('1', 'A→B', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', 'B', '→E 1, 2')
        proof = ProofObj(lines=[line1, line2, line3])
        parser = tflparser.parser
        result = verify_rule(line3, proof, parser)
        self.assertTrue(result.is_valid)

        # Test indirect_proof
        line1 = ProofLineObj('1.1', '¬A', 'Premise')
        line2 = ProofLineObj('1.2', '⊥', 'Premise')
        line3 = ProofLineObj('2', 'A', 'IP 1')
        proof = ProofObj(lines=[line1, line2, line3])
        parser = tflparser.parser
        result = verify_rule(line3, proof, parser)
        self.assertTrue(result.is_valid)

        # Test explosion
        line1 = ProofLineObj('1', '⊥', 'Premise')
        line2 = ProofLineObj('2', 'B', 'X 1')
        proof = ProofObj(lines=[line1, line2])
        parser = tflparser.parser
        result = verify_rule(line2, proof, parser)
        self.assertTrue(result.is_valid)

        # Test iff intro
        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'B', 'Assumption')
        line3 = ProofLineObj('2.1', 'B', 'Assumption')
        line4 = ProofLineObj('2.2', 'A', 'Assumption')
        line5 = ProofLineObj('3', 'A↔B', '↔I 1, 2')
        proof = ProofObj(lines=[line1, line2, line3, line4, line5])
        parser = tflparser.parser
        result = verify_rule(line5, proof, parser)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, None)

        # Test iff elim
        line1 = ProofLineObj('1', 'A↔B', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'Assumption')
        line3 = ProofLineObj('3', 'B', '↔E 1, 2')
        proof = ProofObj(lines=[line1, line2, line3])
        parser = tflparser.parser
        result = verify_rule(line3, proof, parser)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, None)

        # Test reiteration
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'A', 'R 1')
        proof = ProofObj(rules='tfl_derived', lines=[line1, line2])
        parser = tflparser.parser
        result = verify_rule(line2, proof, parser)
        self.assertTrue(result.is_valid)

        # Test double not elim
        line1 = ProofLineObj('1', '¬¬A', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'DNE 1')
        proof = ProofObj(rules='tfl_derived', lines=[line1, line2])
        parser = tflparser.parser
        result = verify_rule(line2, proof, parser)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, None)

class ProofTests(TestCase):

    def test_verify_line_citation(self):
        """
        Verify that the function verify_line_citation is working properly
        """
        # Test with proper input
        line1 = ProofLineObj('2.1', 'A', 'Premise')
        line2 = ProofLineObj('2.2', 'B', 'Premise')
        line3 = ProofLineObj('2.3', 'A∧B', '∧I 1, 2')
        result1 = verify_line_citation(line3.line_no, line1.line_no)
        result2 = verify_line_citation(line3.line_no, line2.line_no)
        self.assertTrue(result1.is_valid)
        self.assertTrue(result2.is_valid)

        # Test with cited line within an unclosed subproof.
        line1 = ProofLineObj('1.1', 'A', 'Premise')
        line2 = ProofLineObj('2.1', 'B', 'Assumption')
        line3 = ProofLineObj('2.2', 'B', 'R')
        line4 = ProofLineObj('3', 'B→B', '→I 2-3')
        line5 = ProofLineObj('4', 'B', '→E 4, 3')
        result = verify_line_citation(line5.line_no, line3.line_no)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg,\
            'Error on line 4: Invalid citation: Line 4 exists within in a subproof at a lower depth than line 2.2')

        # Test with the cited line occurring after the current line
        line1 = ProofLineObj('1', 'A∧B', '∧I 1, 2')
        line2 = ProofLineObj('2', 'B', 'Premise')
        result = verify_line_citation(line1.line_no, line2.line_no)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg,\
            "Error on line 1: Invalid citation: Line 2 occurs after line 1")

        # Test where a line cites a line in a different subproof at same depth
        line1 = ProofLineObj('1.1', 'R', 'Assumption')
        line2 = ProofLineObj('2.1', 'Q', 'Assumption')
        line3 = ProofLineObj('2.2', 'Q∧R', '∧I 1.1, 2.1')
        result = verify_line_citation(line3.line_no, line1.line_no)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'Error on line 2.2: Invalid citation: Line 1.1 occurs in a previous subproof')


    def test_is_conclusion(self):
        """
        Test that the function is_conclusion works properly
        """
        # Test with proper input
        parser = tflparser.parser
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(premises=['A', 'B'], conclusion='A∧B', lines=[line1, line2, line3])
        result = is_conclusion(line3, proof, parser)
        self.assertTrue(result)

        # Test with incomplete proof
        line1 = ProofLineObj('1', '(A∧C)∨(B∧C)', 'Premise')
        line2 = ProofLineObj('2', '(A∧C)', '∨E 1')
        proof = ProofObj(premises='(A∧C)∨(B∧C)', conclusion='C', lines=[line1, line2])
        result = is_conclusion(line2, proof, parser)
        self.assertFalse(result)

        # Test with invalid expression
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(premises=['A', 'B'], conclusion='A∧', lines=[line1, line2, line3])
        result = is_conclusion(line3, proof, parser)
        self.assertFalse(result)

    def test_verify_rule_with_invalid_rule(self):
        """
        Test that verify_rule returns proper error
        if a rule cannot be determined
        """
        line1 = ProofLineObj('1', 'A∧B', 'Premise')
        line2 = ProofLineObj('2', 'A', 'E 1')
        proof = ProofObj(premises='A∧B', conclusion='A', lines=[line1, line2])
        parser = tflparser.parser
        result = verify_rule(line2, proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'Rule "E" on line 2 not found in ruleset "TFL - Basic Rules Only"')

    def test_verify_proof_with_no_lines(self):
        """
        Test that a proof with no lines returns correct error message
        """
        proof = ProofObj(lines=[])
        parser = tflparser.parser
        result = verify_proof(proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "Cannot validate a proof with no lines")

    def test_verify_proof_without_line_nos(self):
        """
        Test that a proof without line numbers returns correct error message
        """
        line1 = ProofLineObj('', 'A', 'Premise')
        proof = ProofObj(lines=[line1])
        parser = tflparser.parser
        result = verify_proof(proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "One or more lines is missing a line number")

    def test_verify_proof_without_expression(self):
        """
        Test that a proof without an expression returns correct error message
        """
        line1 = ProofLineObj('1', '', 'Premise')
        proof = ProofObj(lines=[line1])
        parser = tflparser.parser
        result = verify_proof(proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "No expression on line 1")

    def test_verify_proof_with_invalid_rule(self):
        """
        Test that a proof with an invalid rule returns correct error message
        """
        line1 = ProofLineObj('1', 'A∧B', 'Premise')
        line2 = ProofLineObj('2', 'C', '∧E 1')
        proof = ProofObj(premises = 'A∧B', lines=[line1, line2])
        parser = tflparser.parser
        result = verify_proof(proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "Error on line 2: Line 2 does not follow from line 1")

    def test_verify_proof_with_assumption_as_conclusion(self):
        """
        Test that a proof attempting to conclude with assumption
        returns the correct error message
        """
        line1 = ProofLineObj('1', '(A∧C)∨(B∧C)', 'Premise')
        line2 = ProofLineObj('2.1', 'C', 'Assumption')
        proof = ProofObj(premises='(A∧C)∨(B∧C)', conclusion='C', lines=[line1, line2])
        parser = tflparser.parser
        result = verify_proof(proof, parser)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, "Proof cannot be concluded with an assumption")

    def test_verify_proof_with_conclusion_in_subproof(self):
        """
        Test that a proof attempting to conclude within a subproof
        returns the correct error message
        """
        line1 = ProofLineObj('1', '(A∧C)∨(B∧C)', 'Premise')
        line2 = ProofLineObj('2.1', 'A∧C', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', '∧E 2.1')
        proof = ProofObj(premises='(A∧C)∨(B∧C)', conclusion='C', lines=[line1, line2, line3])
        parser = tflparser.parser
        result = verify_proof(proof, parser)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, "Proof cannot be concluded within a subproof")            

    def test_verify_proof_with_valid_proof(self):
        """
        Test that the verify_proof function returns is_valid == True
        when provided with a valid proof
        """
        # And Intro
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(premises=['A', 'B'], conclusion='A∧B', lines=[line1, line2, line3])
        parser = tflparser.parser
        result = verify_proof(proof, parser)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, None)

        # And Elim
        line1 = ProofLineObj('1', 'A∧B', 'Premise')
        line2 = ProofLineObj('2', 'A', '∧E 1')
        proof = ProofObj(premises='A∧B', conclusion='A', lines=[line1, line2])
        parser = tflparser.parser
        result = verify_proof(proof, parser)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, None)

        # Or Intro/Elim
        line1 = ProofLineObj('1', 'AvB', 'Premise')
        line2 = ProofLineObj('2.1', 'A', 'Assumption')
        line3 = ProofLineObj('2.2', 'AvB', 'vI 2.1')
        line4 = ProofLineObj('3.1', 'B', 'Assumption')
        line5 = ProofLineObj('3.2', 'AvB', 'vI 3.1')
        line6 = ProofLineObj('4', 'AvB', 'vE 1, 2, 3')
        proof = ProofObj(premises='AvB', conclusion='AvB', lines=[line1, line2, line3, line4, line5, line6])
        parser = tflparser.parser
        result = verify_proof(proof, parser)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, None)


    def test_verify_proof_with_invalid_proof(self):
        """
        Test that the verify_proof function returns is_valid == False
        when provided with an invalid proof
        (and that the err_msg is appropriate)
        """
        # Test a proof with an invalid character
        line1 = ProofLineObj('1', 'Hello', 'Premise')
        proof = ProofObj(premises='Hello', lines=[line1])
        parser = tflparser.parser
        result = verify_proof(proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, "Illegal character 'e' on line 1")

        # Test a proof with an valid characters but invalid syntax
        line1 = ProofLineObj('1', 'A∧', 'Premise')
        proof = ProofObj(premises='A∧', lines=[line1])
        parser = tflparser.parser
        result = verify_proof(proof, parser)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.err_msg, 'Syntax error on line 1.  Expression "A∧" does not conform to ruleset "TFL - Basic Rules Only"')
    
        # Test with a valid but incomplete proof
        line1 = ProofLineObj('1', '(A∧C)∨(B∧C)', 'Premise')
        line2 = ProofLineObj('2.1', '(A∧C)', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', '∧E 2.1')
        proof = ProofObj(premises='(A∧C)∨(B∧C)', conclusion='C', lines=[line1, line2])
        parser = tflparser.parser
        result = verify_proof(proof, parser)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.err_msg, "All lines are valid, but the proof is incomplete")


