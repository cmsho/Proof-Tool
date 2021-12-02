from django.test import TestCase
from django.urls import reverse

from .proof import ProofObj, ProofLineObj, get_line_no, get_line_nos, get_lines_in_subproof, is_conclusion, verify_and_intro, verify_and_elim, verify_assumption, verify_double_not_elim, verify_iff_elim, verify_iff_intro, verify_line_citation, verify_explosion, verify_or_intro, \
    verify_or_elim, verify_implies_intro, verify_implies_elim, verify_not_intro, \
    verify_not_elim, verify_indirect_proof, verify_premise, verify_reiteration, verify_rule, verify_proof, depth

# Create your tests here.

class ProofTests(TestCase):

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
    
    def test_get_lines_in_subproof(self):
        """
        Test that the get_lines_in_subproof method is working properly
        """
        line1 = ProofLineObj('1', '(A∧C)∨(B∧C)', 'Premise')
        line2_1 = ProofLineObj('2.1', '(A∧C)', 'Assumption')
        line2_2 = ProofLineObj('2.2', 'C', '∧E 2.1')
        line3_1 = ProofLineObj('3.1', '(B∧C)', 'Assumption')
        line3_2 = ProofLineObj('3.2', 'C', '∧E 2.1')
        line4 = ProofLineObj('4', 'C', '∨E, 1, 2, 3')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2_1, line2_2, line3_1, line3_2, line4])
        result = get_lines_in_subproof('2', proof)
        self.assertEqual(result, [line2_1, line2_2])


    def test_proof_line(self):
        """
        Test that a ProofLine can be constructed appropriately
        """
        line1 = ProofLineObj('1', '(A∧C)∨(B∧C)', 'Premise')
        self.assertEqual('1', line1.line_no)
        self.assertEqual('(A∧C)∨(B∧C)', line1.expression)
        self.assertEqual('Premise', line1.rule)
    
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
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2_1, line2_2, line3_1, line3_2, line4])
        self.assertEqual(len(proof.lines), 6)

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

    def test_verify_line_citation(self):
        """
        Verify that the function verify_line_citation is working properly
        """
        # Test with proper input
        line1 = ProofLineObj('2.1', 'A', 'Premise')
        line2 = ProofLineObj('2.2', 'B', 'Premise')
        line3 = ProofLineObj('2.3', 'A∧B', '∧I 1, 2')
        result1 = verify_line_citation(line3, line1)
        result2 = verify_line_citation(line3, line2)
        self.assertEqual(result1.is_valid, True)
        self.assertEqual(result2.is_valid, True)

        # Test with cited line within an unclosed subproof.
        line1 = ProofLineObj('1.1', 'A', 'Premise')
        line2 = ProofLineObj('2.1', 'B', 'Assumption')
        line3 = ProofLineObj('2.2', 'B', 'R')
        line4 = ProofLineObj('3', 'B→B', '→I 2-3')
        line5 = ProofLineObj('4', 'B', '→E 4, 3')
        result = verify_line_citation(line5, line3)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg,\
            'Line 2.2 occurs within a subproof that has not been closed prior to line 4')

        # Test with the cited line occurring after the current line
        line1 = ProofLineObj('2.1', 'A∧B', '∧I 1, 2')
        line2 = ProofLineObj('2.2', 'B', 'Premise')
        result = verify_line_citation(line1, line2)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg,\
            "Invalid citation: line 2.2 occurs after line 2.1")

        # Test with line numbers not formatted properly
        line1 = ProofLineObj('1', 'A∧B', '∧I 1, 2')
        line2 = ProofLineObj('2.a', 'B', 'Premise')
        result = verify_line_citation(line1, line2)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg,\
            "Line numbers are not formatted properly")

    def test_is_conclusion(self):
        """
        Test that the function is_conclusion works properly
        """
        # Test with proper input
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(premises=['A', 'B'], conclusion='A∧B', lines=[])
        proof.lines.extend([line1, line2, line3])
        result = is_conclusion(line3, proof)
        self.assertEqual(result, True)

        # Test with incomplete proof
        line1 = ProofLineObj('1', '(A∧C)∨(B∧C)', 'Premise')
        line2 = ProofLineObj('2', '(A∧C)', '∨E 1')
        proof = ProofObj(premises='(A∧C)∨(B∧C)', conclusion='C', lines=[])
        proof.lines.extend([line1, line2])
        result = is_conclusion(line2, proof)
        self.assertEqual(result, False)

    def test_verify_premise(self):
        """
        Test that the function verify_premise is working properly
        """
        # Test with proper input
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(premises=['A', 'B'], lines=[])
        proof.lines.extend([line1, line2, line3])
        result1 = verify_premise(line1, proof)
        result2 = verify_premise(line2, proof)
        self.assertEqual(result1.is_valid, True)
        self.assertEqual(result2.is_valid, True)
    
        # Test with a line not in premises    
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(premises='A', lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_premise(line2, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Expression on line 2 is not a premise")

    def test_verify_assumption(self):
        """
        Test that the function verify_assumption is working properly
        """
        # Test with valid input
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2.1', 'B', 'Assumption')
        line3 = ProofLineObj('2.2', 'A∧B', '∧I 1, 2')
        proof = ProofObj(premises='A', lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_assumption(line2)
        self.assertEqual(result.is_valid, True)

        # Test with invalid input
        # Test with valid input
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2.1', 'B', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', 'Assumption')
        proof = ProofObj(premises='A', lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_assumption(line3)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'Assumptions can only exist at the start of a subproof')

    def test_verify_explosion(self):
        """
        Test that the function verify_explosion is working properly
        """
        # Test with proper input
        line1 = ProofLineObj('1', '⊥', 'Premise')
        line2 = ProofLineObj('2', 'B', 'X 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_explosion(line2, proof)
        self.assertEqual(result.is_valid, True)

        # Test without contradiction
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'X 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_explosion(line2, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line 1 should be '⊥' (Contradiction)")

    def test_verify_reiteration(self):
        """
        Test that the function verify_reiteration is working properly
        """
        # Test with proper input
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'A', 'R 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_reiteration(line2, proof)
        self.assertEqual(result.is_valid, True)

        # Test with unequivalent expressions
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'R 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_reiteration(line2, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'Lines 1 and 2 are not equivalent')        

    def test_verify_and_intro(self):
        """
        Test that the function verify_and_intro is working properly
        """
        # Test with proper input
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_and_intro(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test with invalid conjunction
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'C', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_and_intro(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "The conjunction of lines 1 and 2 does not equal line 3")

        # Test with invalid line specification
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_and_intro(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line numbers are not specified correctly.  Conjunction Introduction: ∧I m, n")        

    def test_verify_and_elim(self):
        """
        Test that the function verify_and_elim is working properly
        """
        # Test with proper input
        line1 = ProofLineObj('1', 'A∧B', 'Premise')
        line2 = ProofLineObj('2', 'A', '∧E 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_and_elim(line2, proof)
        self.assertEqual(result.is_valid, True)

        line1 = ProofLineObj('1', '(A∧C)∨(B∧C)', 'Premise')
        line2 = ProofLineObj('2.1', 'A∧C', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', '∧E 2.1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_and_elim(line3, proof)
        self.assertEqual(result.is_valid, True) 

        # Test with invalid conclusion
        line1 = ProofLineObj('1', 'A∧B', 'Premise')
        line2 = ProofLineObj('2', 'C', '∧E 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_and_elim(line2, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line 2 does not follow from line 1")
    
    def test_verify_or_intro(self):
        """
        Test that the function verify_or_intro is working properly
        """
        # Test with valid input
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'A∨B', '∨I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_or_intro(line2, proof)
        self.assertEqual(result.is_valid, True)

        # Test with invalid conclusion
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B∨C', '∨I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_or_intro(line2, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line 2 does not follow from line 1")

    def test_verify_or_elim(self):
        """
        Test that the function verify_or_elim is working properly
        """
        # Test with valid input
        line1 = ProofLineObj('1', 'A∨B', 'Premise')
        line2 = ProofLineObj('2.1', 'A', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', 'Assumption')
        line4 = ProofLineObj('3.1', 'B', 'Assumption')
        line5 = ProofLineObj('3.2', 'C', 'Assumption')
        line6 = ProofLineObj('4', 'C', '∨E 1, 2, 3')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = verify_or_elim(line6, proof)
        self.assertEqual(result.is_valid, True)

        # Test with valid input
        line1 = ProofLineObj('1', 'A∨B', 'Premise')
        line2 = ProofLineObj('2.1', 'A', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', 'Assumption')
        line4 = ProofLineObj('3.1', 'B', 'Assumption')
        line5 = ProofLineObj('3.2', 'C', 'Assumption')
        line6 = ProofLineObj('4', 'C', '∨E 1, 2, 3')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = verify_or_elim(line6, proof)
        self.assertEqual(result.is_valid, True)

        # Test with unequivalent expressions
        line1 = ProofLineObj('1', 'A∨B', 'Premise')
        line2 = ProofLineObj('2.1', 'A', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', 'Assumption')
        line4 = ProofLineObj('3.1', 'B', 'Assumption')
        line5 = ProofLineObj('3.2', 'D', 'Assumption')
        line6 = ProofLineObj('4', 'C', '∨E 1, 2, 3')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = verify_or_elim(line6, proof)
        self.assertEqual(result.is_valid, False)
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
        result = verify_or_elim(line6, proof)
        self.assertEqual(result.is_valid, False)
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
        result = verify_or_elim(line6, proof)
        self.assertEqual(result.is_valid, False)
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
        result = verify_or_elim(line6, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "The expressions on lines 2.1 and 3.1 should be different")

    def test_verify_not_intro(self):
        """
        Test that the function verify_not_intro is working properly
        """
        # Test with valid input
        line1 = ProofLineObj('1.1', 'A', 'Premise')
        line2 = ProofLineObj('1.2', '⊥', 'Premise')
        line3 = ProofLineObj('2', '¬A', '¬I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_intro(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test without contradiction
        line1 = ProofLineObj('1.1', 'A', 'Premise')
        line2 = ProofLineObj('1.2', 'B', 'Premise')
        line3 = ProofLineObj('2', '¬A', '¬I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_intro(line3, proof)
        self.assertEqual(result.is_valid, False)   
        self.assertEqual(result.err_msg, "Line 1.2 should be '⊥' (Contradiction)")

        # Test without proper negation
        line1 = ProofLineObj('1.1', 'A', 'Premise')
        line2 = ProofLineObj('1.2', '⊥', 'Premise')
        line3 = ProofLineObj('2', '¬B', '¬I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_intro(line3, proof)
        self.assertEqual(result.is_valid, False)   
        self.assertEqual(result.err_msg, "Line 2 is not the negation of line 1.1")

    def test_verify_not_elim(self):
        """
        Test that the fucntion verify_not_elim is working properly
        """
        # Test with valid input
        line1 = ProofLineObj('1', '¬A', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', '⊥', '¬E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_elim(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test without contradiction
        line1 = ProofLineObj('1', '¬A', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', 'B', '¬E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_elim(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line 3 should be '⊥' (Contradiction)")

        # Test without proper contradiction
        line1 = ProofLineObj('1', '¬A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', '⊥', '¬E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_elim(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line 1 is not the negation of line 2")

        # Test with improper line specification
        line1 = ProofLineObj('1', '¬A', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', '⊥', '¬E 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_elim(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line numbers are not specified correctly.  Negation Elimination: ¬E m, n")


    def test_verify_implies_intro(self):
        """
        Test that the function verify_implies_intro is working properly
        """
        # Test with valid input
        line1 = ProofLineObj('1.1', 'A∧B', 'Premise')
        line2 = ProofLineObj('1.2', 'B', '∧E 1.1')
        line3 = ProofLineObj('2', '(A∧B)→B', '→I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_implies_intro(line3, proof)
        self.assertEqual(result.is_valid, True)

        # # Test with invalid implication
        # line1 = ProofLineObj('1', 'A', 'Assumption')
        # line2 = ProofLineObj('2', 'B', 'Assumption')
        # line3 = ProofLineObj('3', 'A→C', '→I 1')
        # proof = ProofObj(lines=[])
        # proof.lines.extend([line1, line2, line3])
        # result = verify_implies_intro(line3, proof)
        # self.assertEqual(result.is_valid, False)
        # self.assertEqual(result.err_msg, 'The expressions on lines 1 and 2 do not match the implication on line 3')

        # # Test with improper line specification
        # line1 = ProofLineObj('1', 'A', 'Assumption')
        # line2 = ProofLineObj('2', 'B', 'Assumption')
        # line3 = ProofLineObj('3', 'A→B', '→I 2')
        # proof = ProofObj(lines=[])
        # proof.lines.extend([line1, line2, line3])
        # result = verify_implies_intro(line3, proof)
        # self.assertEqual(result.is_valid, False)
        # self.assertEqual(result.err_msg, 'Line numbers are not specified correctly.  Conditional Introduction: →I m-n')

    def test_verify_implies_elim(self):
        """
        Test that the function verify_implies_elim is working properly
        """
        # Test with valid input
        line1 = ProofLineObj('1', 'A→B', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', 'B', '→E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_implies_elim(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test with invalid elimination
        line1 = ProofLineObj('1', 'A→B', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', 'C', '→E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_implies_elim(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'The expressions on lines 2 and 3 do not match the implication on line 1')

        # Test with improper line specification
        line1 = ProofLineObj('1', 'A→B', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', 'B', '→E 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_implies_elim(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'Line numbers are not specified correctly.  Conditional Elimination (Modus Ponens): →E m, n')

    def test_verify_indirect_proof(self):
        """
        Test that the function verify_indirect_proof is working properly
        """
        # Test with valid input
        line1 = ProofLineObj('1.1', '¬A', 'Premise')
        line2 = ProofLineObj('1.2', '⊥', 'X')
        line3 = ProofLineObj('2', 'A', 'IP 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_indirect_proof(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test without contradition
        line1 = ProofLineObj('1.1', '¬A', 'Premise')
        line2 = ProofLineObj('1.2', 'B', 'Premise')
        line3 = ProofLineObj('2', 'A', 'IP 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_indirect_proof(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line 1.2 should be '⊥' (Contradiction)")

        # Test with improper negation
        line1 = ProofLineObj('1.1', '¬A', 'Premise')
        line2 = ProofLineObj('1.2', '⊥', 'Premise')
        line3 = ProofLineObj('2', 'B', 'IP 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_indirect_proof(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line 1.1 is not the negation of line 2")

    def test_verify_iff_intro(self):
        """
        Test that the verify_iff_intro function is working properly
        """
        # Test with valid input
        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'B', 'Assumption')
        line3 = ProofLineObj('2.1', 'B', 'Assumption')
        line4 = ProofLineObj('2.2', 'A', 'Assumption')
        line5 = ProofLineObj('3', 'A↔B', '↔I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5])
        result = verify_iff_intro(line5, proof)
        self.assertEqual(result.is_valid, True)
        self.assertEqual(result.err_msg, None)

        # Test with unequivalent expressions
        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'C', 'Assumption')
        line3 = ProofLineObj('2.1', 'B', 'Assumption')
        line4 = ProofLineObj('2.2', 'A', 'Assumption')
        line5 = ProofLineObj('3', 'A↔B', '↔I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5])
        result = verify_iff_intro(line5, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'The expressions on lines 1.2 and 2.1 are not equivalent')

        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'B', 'Assumption')
        line3 = ProofLineObj('2.1', 'B', 'Assumption')
        line4 = ProofLineObj('2.2', 'C', 'Assumption')
        line5 = ProofLineObj('3', 'A↔B', '↔I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5])
        result = verify_iff_intro(line5, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'The expressions on lines 1.1 and 2.2 are not equivalent')

        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'B', 'Assumption')
        line3 = ProofLineObj('2.1', 'B', 'Assumption')
        line4 = ProofLineObj('2.2', 'A', 'Assumption')
        line5 = ProofLineObj('3', 'C↔B', '↔I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5])
        result = verify_iff_intro(line5, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'Left side of line 3 does not equal either of the expressions on lines 1.2 and 2.2')

        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'B', 'Assumption')
        line3 = ProofLineObj('2.1', 'B', 'Assumption')
        line4 = ProofLineObj('2.2', 'A', 'Assumption')
        line5 = ProofLineObj('3', 'A↔C', '↔I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5])
        result = verify_iff_intro(line5, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'Right side of line 3 does not equal either of the expressions on lines 1.2 and 2.2')

        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'A', 'Assumption')
        line3 = ProofLineObj('2.1', 'A', 'Assumption')
        line4 = ProofLineObj('2.2', 'A', 'Assumption')
        line5 = ProofLineObj('3', 'A↔B', '↔I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5])
        result = verify_iff_intro(line5, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'Invalid introduction on line 3')

    def test_verify_iff_elim(self):
        """
        Test that the verify_iff_elim function is working properly
        """
        # Test with valid input
        line1 = ProofLineObj('1', 'A↔B', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'Assumption')
        line3 = ProofLineObj('3', 'B', '↔E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_iff_elim(line3, proof)
        self.assertEqual(result.is_valid, True)
        self.assertEqual(result.err_msg, None)

        line1 = ProofLineObj('1', 'A↔B', 'Assumption')
        line2 = ProofLineObj('2', 'B', 'Assumption')
        line3 = ProofLineObj('3', 'A', '↔E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_iff_elim(line3, proof)
        self.assertEqual(result.is_valid, True)
        self.assertEqual(result.err_msg, None)

        # Test with invalid input
        line1 = ProofLineObj('1', 'A↔B', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'Assumption')
        line3 = ProofLineObj('3', 'A', '↔E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_iff_elim(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "The expressions on lines 2 and 3 do not represent both the left and right side of the expression on line 1")

        # Test with invalid input
        line1 = ProofLineObj('1', 'A↔B', 'Assumption')
        line2 = ProofLineObj('2', 'C', 'Assumption')
        line3 = ProofLineObj('3', 'A', '↔E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_iff_elim(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "The expression on line 2 does not represent the left or right side of the expression on line 1")

        # Test with invalid input
        line1 = ProofLineObj('1', 'A↔B', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'Assumption')
        line3 = ProofLineObj('3', 'C', '↔E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_iff_elim(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "The expression on line 3 does not represent the left or right side of the expression on line 1")

    def test_verify_double_not_elim(self):
        """
        Test that the verify_double_not_elim function is working properly
        """
        # Test with valid input
        line1 = ProofLineObj('1', '¬¬A', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'DNE 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_double_not_elim(line2, proof)
        self.assertEqual(result.is_valid, True)
        self.assertEqual(result.err_msg, None)

        # Test with invalid input
        line1 = ProofLineObj('1', '¬¬A', 'Assumption')
        line2 = ProofLineObj('2', 'B', 'DNE 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_double_not_elim(line2, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'Lines 1 and 2 are not equivalent')

        # Test with invalid input
        line1 = ProofLineObj('1', '¬A', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'DNE 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_double_not_elim(line2, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'Line 1 is not an instance of double-not operators')

        # Test with invalid input
        line1 = ProofLineObj('1', 'A^B', 'Assumption')
        line2 = ProofLineObj('2', 'A', 'DNE 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_double_not_elim(line2, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "The main logical operator on line 1 is not '¬'")                


    def test_verify_rule(self):
        """
        Test that the verify_rule function is working properly
        """
        # Test and_intro
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_rule(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test and_elim
        line1 = ProofLineObj('1', 'A∧B', 'Premise')
        line2 = ProofLineObj('2', 'A', '∧E 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_rule(line2, proof)
        self.assertEqual(result.is_valid, True)

        # Test or_intro
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'A∨B', '∨I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_rule(line2, proof)
        self.assertEqual(result.is_valid, True)

        # Test or_elim
        line1 = ProofLineObj('1', 'A∨B', 'Premise')
        line2 = ProofLineObj('2.1', 'A', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', 'Assumption')
        line4 = ProofLineObj('3.1', 'B', 'Assumption')
        line5 = ProofLineObj('3.2', 'C', 'Assumption')
        line6 = ProofLineObj('4', 'C', '∨E 1, 2, 3')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = verify_rule(line6, proof)
        self.assertEqual(result.is_valid, True)

        # Test not_intro
        line1 = ProofLineObj('1.1', 'A', 'Premise')
        line2 = ProofLineObj('1.2', '⊥', 'Premise')
        line3 = ProofLineObj('2', '¬A', '¬I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_rule(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test not_elim
        line1 = ProofLineObj('1', '¬A', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', '⊥', '¬E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_rule(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test implies_intro
        line1 = ProofLineObj('1.1', 'A', 'Assumption')
        line2 = ProofLineObj('1.2', 'B', 'Assumption')
        line3 = ProofLineObj('2', 'A→B', '→I 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_rule(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test implies_elim
        line1 = ProofLineObj('1', 'A→B', 'Premise')
        line2 = ProofLineObj('2', 'A', 'Premise')
        line3 = ProofLineObj('3', 'B', '→E 1, 2')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_rule(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test indirect_proof
        line1 = ProofLineObj('1.1', '¬A', 'Premise')
        line2 = ProofLineObj('1.2', '⊥', 'Premise')
        line3 = ProofLineObj('2', 'A', 'IP 1')
        proof = ProofObj(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_rule(line3, proof)
        self.assertEqual(result.is_valid, True)


    def test_verify_proof_with_valid_proof(self):
        """
        Test that the verify_proof function returns is_valid == True
        when provided with a valid proof
        """
        # And Intro
        line1 = ProofLineObj('1', 'A', 'Premise')
        line2 = ProofLineObj('2', 'B', 'Premise')
        line3 = ProofLineObj('3', 'A∧B', '∧I 1, 2')
        proof = ProofObj(premises=['A', 'B'], conclusion='A∧B', lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, True)
        self.assertEqual(result.err_msg, None)

        # And Elim
        line1 = ProofLineObj('1', 'A∧B', 'Premise')
        line2 = ProofLineObj('2', 'A', '∧E 1')
        proof = ProofObj(premises='A∧B', conclusion='A', lines=[])
        proof.lines.extend([line1, line2])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, True)
        self.assertEqual(result.err_msg, None)

        # Or Intro/Elim
        line1 = ProofLineObj('1', 'AvB', 'Premise')
        line2 = ProofLineObj('2.1', 'A', 'Assumption')
        line3 = ProofLineObj('2.2', 'AvB', 'vI 2.1')
        line4 = ProofLineObj('3.1', 'B', 'Assumption')
        line5 = ProofLineObj('3.2', 'AvB', 'vI 3.1')
        line6 = ProofLineObj('4', 'AvB', 'vE 1, 2, 3')
        proof = ProofObj(premises='AvB', conclusion='AvB', lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, True)
        self.assertEqual(result.err_msg, None)


    def test_verify_proof_with_invalid_proof(self):
        """
        Test that the verify_proof function returns is_valid == False
        when provided with an invalid proof
        (and that the err_msg is appropriate)
        """
        # Test a proof with an invalid character
        line1 = ProofLineObj('1', 'Hello', 'Premise')
        proof = ProofObj(premises='Hello', lines=[])
        proof.lines.extend([line1])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Illegal character 'e' on line 1")

        # Test a proof with an valid characters but invalid syntax
        line1 = ProofLineObj('1', 'A∧', 'Premise')
        proof = ProofObj(premises='A∧', lines=[])
        proof.lines.extend([line1])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Syntax error on line 1")
    
        # Test with a valid but incomplete proof
        line1 = ProofLineObj('1', '(A∧C)∨(B∧C)', 'Premise')
        line2 = ProofLineObj('2.1', '(A∧C)', 'Assumption')
        line3 = ProofLineObj('2.2', 'C', '∧E 2.1')
        proof = ProofObj(premises='(A∧C)∨(B∧C)', conclusion='C', lines=[])
        proof.lines.extend([line1, line2])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, True)
        self.assertEqual(result.err_msg, "All lines are valid, but the proof is incomplete")


