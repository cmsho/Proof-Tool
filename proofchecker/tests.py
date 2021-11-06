from django.test import TestCase

from .proof import Proof, ProofLine, verify_and_intro, verify_and_elim, verify_indirect_proof, verify_or_intro, verify_or_elim, \
    verify_implies_intro, verify_implies_elim, verify_not_intro, verify_not_elim, verify_indirect_proof, verify_rule, verify_proof
from .syntax import Syntax
from .utils import tflparse as yacc
from .utils.binarytree import Node, tree_to_string, string_to_tree

# Create your tests here.

class BinaryTreeTests(TestCase):

    def test_node_equivalence(self):
        """
        Should return true when comparing two separate nodes 
        that represent binary trees with identical values
        """
        a = Node('^')
        a.left = Node('A')
        a.right = Node('B')

        b = Node('v')
        b.left = Node('^')
        b.left.left = Node('A')
        b.left.right = Node('B')
        b.right = Node('C')

        c = yacc.parser.parse('A∧B')
        d = yacc.parser.parse('(A∧B)∨[(¬C→D)∧(A↔Z)]')

        self.assertEqual(a, b.left)
        self.assertEqual(c, d.left)

        e = yacc.parser.parse('A∧B')
        f = yacc.parser.parse('A∧B')

        # FIXME: Two different characters representing same symbol cause failure
        # self.assertEqual(e, f)
    
    def test_tree_to_string(self):
        """
        Should construct an unambiguous string representation
        of the binary tree
        """
        a = yacc.parser.parse('(A∧B)∨C')
        b = yacc.parser.parse('A∧(B∨C)')

        c = []
        d = []
        tree_to_string(a, c)
        tree_to_string(b, d)
        
        self.assertEqual(''.join(c), '∨(∧(A)(B))(C)')
        self.assertEqual(''.join(d), '∧(A)(∨(B)(C))')
    
    def test_string_to_tree(self):
        """
        Should construct a binary tree from an
        unambigious string representation
        """
        a = '∨(∧(A)(B))(C)'

        b = string_to_tree(a)
        c = yacc.parser.parse('(A∧B)∨C')
        
        self.assertTrue(b.value == '∨')
        self.assertEqual(b, c)

class ProofTests(TestCase):
    
    def test_proof_line(self):
        """
        Test that a ProofLine can be constructed appropriately
        """
        line1 = ProofLine(1, '(A∧C)∨(B∧C)', 'Premise')
        self.assertEqual(1, line1.line_no)
        self.assertEqual('(A∧C)∨(B∧C)', line1.expression)
        self.assertEqual('Premise', line1.rule)
    
    def test_proof_construction(self):
        """
        Test that a Proof can be constructed appropriately
        """
        line1 = ProofLine(1, '(A∧C)∨(B∧C)', 'Premise')
        line2_1 = ProofLine(2.1, '(A∧C)', 'Assumption')
        line2_2 = ProofLine(2.2, 'C', '∧E 2.1')
        line3_1 = ProofLine(3.1, '(B∧C)', 'Assumption')
        line3_2 = ProofLine(3.2, 'C', '∧E 2.1')
        line4 = ProofLine(4, 'C', '∨E, 1, 2, 3')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2_1, line2_2, line3_1, line3_2, line4])
        self.assertEqual(len(proof.lines), 6)
    
    def test_verify_and_intro(self):
        """
        Test that the function verify_and_intro is working properly
        """
        # Test with proper input
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, 'B', 'Premise')
        line3 = ProofLine(3, 'A∧B', '∧I 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_and_intro(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test with invalid conjunction
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, 'C', 'Premise')
        line3 = ProofLine(3, 'A∧B', '∧I 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_and_intro(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "The conjunction of lines 1 and 2 does not equal line 3")

        # Test with invalid line specification
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, 'B', 'Premise')
        line3 = ProofLine(3, 'A∧B', '∧I 1')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_and_intro(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line numbers are not specified correctly.  Conjunction Introduction: ∧I m, n")        

    def test_verify_and_elim(self):
        """
        Test that the function verify_and_elim is working properly
        """
        # Test with proper input
        line1 = ProofLine(1, 'A∧B', 'Premise')
        line2 = ProofLine(2, 'A', '∧E 1')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_and_elim(line2, proof)
        self.assertEqual(result.is_valid, True)

        # Test with invalid conclusion
        line1 = ProofLine(1, 'A∧B', 'Premise')
        line2 = ProofLine(2, 'C', '∧E 1')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_and_elim(line2, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line 2 does not follow from line 1")

        # Test with invalid line specification
        line1 = ProofLine(1, 'A∧B', 'Premise')
        line2 = ProofLine(2, 'A', '∧E 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_and_elim(line2, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line numbers are not specified correctly.  Conjunction Elimination: ∧E m")
    
    def test_verify_or_intro(self):
        """
        Test that the function verify_or_intro is working properly
        """
        # Test with valid input
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, 'A∨B', '∨I 1')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_or_intro(line2, proof)
        self.assertEqual(result.is_valid, True)

        # Test with invalid conclusion
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, 'B∨C', '∨I 1')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_or_intro(line2, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line 2 does not follow from line 1")

        # Test with invalid line specification
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, 'A∨B', '∨I 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_or_intro(line2, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line numbers are not specified correctly.  Disjunction Introduction: ∨I m")

    def test_verify_or_elim(self):
        """
        Test that the function verify_or_elim is working properly
        TODO: Verify that it is legal to reference a line number
        """
        # Test with valid input
        line1 = ProofLine(1, 'A∨B', 'Premise')
        line2 = ProofLine(2, 'A', 'Assumption')
        line3 = ProofLine(3, 'C', 'Assumption')
        line4 = ProofLine(4, 'B', 'Assumption')
        line5 = ProofLine(5, 'C', 'Assumption')
        line6 = ProofLine(6, 'C', '∨E 1, 2-3, 4-5')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = verify_or_elim(line6, proof)
        self.assertEqual(result.is_valid, True)

        # Test with unequivalent expressions
        line1 = ProofLine(1, 'A∨B', 'Premise')
        line2 = ProofLine(2, 'A', 'Assumption')
        line3 = ProofLine(3, 'C', 'Assumption')
        line4 = ProofLine(4, 'B', 'Assumption')
        line5 = ProofLine(5, 'D', 'Assumption')
        line6 = ProofLine(6, 'C', '∨E 1, 2-3, 4-5')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = verify_or_elim(line6, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "The expressions on lines 3, 5 and 6 are not equivalent")

        # Test with improper disjunction
        line1 = ProofLine(1, 'A∨B', 'Premise')
        line2 = ProofLine(2, 'A', 'Assumption')
        line3 = ProofLine(3, 'C', 'Assumption')
        line4 = ProofLine(4, 'D', 'Assumption')
        line5 = ProofLine(5, 'C', 'Assumption')
        line6 = ProofLine(6, 'C', '∨E 1, 2-3, 4-5')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = verify_or_elim(line6, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "The expression on line 4 is not part of the disjunction on line 1")

        # Test with improper disjunction
        line1 = ProofLine(1, 'A∨B', 'Premise')
        line2 = ProofLine(2, 'D', 'Assumption')
        line3 = ProofLine(3, 'C', 'Assumption')
        line4 = ProofLine(4, 'B', 'Assumption')
        line5 = ProofLine(5, 'C', 'Assumption')
        line6 = ProofLine(6, 'C', '∨E 1, 2-3, 4-5')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = verify_or_elim(line6, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "The expression on line 2 is not part of the disjunction on line 1")

        # Test with only one half of disjunction
        line1 = ProofLine(1, 'A∨B', 'Premise')
        line2 = ProofLine(2, 'A', 'Assumption')
        line3 = ProofLine(3, 'C', 'Assumption')
        line4 = ProofLine(4, 'A', 'Assumption')
        line5 = ProofLine(5, 'C', 'Assumption')
        line6 = ProofLine(6, 'C', '∨E 1, 2-3, 4-5')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = verify_or_elim(line6, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "The expressions on lines 2 and 4 should be different")

        # Test with improper line specification
        line1 = ProofLine(1, 'A∨B', 'Premise')
        line2 = ProofLine(2, 'A', 'Assumption')
        line3 = ProofLine(3, 'C', 'Assumption')
        line4 = ProofLine(4, 'A', 'Assumption')
        line5 = ProofLine(5, 'C', 'Assumption')
        line6 = ProofLine(6, 'C', '∨E 1, 2-5')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = verify_or_elim(line6, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line numbers are not specified correctly.  Disjunction Elimination: ∨E m, i-j, k-l")

    def test_verify_not_intro(self):
        """
        Test that the function verify_not_intro is working properly
        """
        # Test with valid input
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, '⊥', 'Premise')
        line3 = ProofLine(3, '¬A', '¬I 1-2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_intro(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test without contradiction
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, 'B', 'Premise')
        line3 = ProofLine(3, '¬A', '¬I 1-2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_intro(line3, proof)
        self.assertEqual(result.is_valid, False)   
        self.assertEqual(result.err_msg, "Line 2 should be '⊥' (Contradiction)")

        # Test without proper negation
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, '⊥', 'Premise')
        line3 = ProofLine(3, '¬B', '¬I 1-2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_intro(line3, proof)
        self.assertEqual(result.is_valid, False)   
        self.assertEqual(result.err_msg, "Line 3 is not the negation of line 1")
        
        # Test with improper line specification
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, '⊥', 'Premise')
        line3 = ProofLine(3, '¬A', '¬I 1')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_intro(line3, proof)
        self.assertEqual(result.is_valid, False)   
        self.assertEqual(result.err_msg, "Line numbers are not specified correctly.  Negation Introduction: ¬I m-n")

    def test_verify_not_elim(self):
        """
        Test that the fucntion verify_not_elim is working properly
        """
        # Test with valid input
        line1 = ProofLine(1, '¬A', 'Premise')
        line2 = ProofLine(2, 'A', 'Premise')
        line3 = ProofLine(3, '⊥', '¬E 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_elim(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test without contradiction
        line1 = ProofLine(1, '¬A', 'Premise')
        line2 = ProofLine(2, 'A', 'Premise')
        line3 = ProofLine(3, 'B', '¬E 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_elim(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line 3 should be '⊥' (Contradiction)")

        # Test without proper contradiction
        line1 = ProofLine(1, '¬A', 'Premise')
        line2 = ProofLine(2, 'B', 'Premise')
        line3 = ProofLine(3, '⊥', '¬E 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_elim(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line 1 is not the negation of line 2")

        # Test with improper line specification
        line1 = ProofLine(1, '¬A', 'Premise')
        line2 = ProofLine(2, 'A', 'Premise')
        line3 = ProofLine(3, '⊥', '¬E 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_not_elim(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line numbers are not specified correctly.  Negation Elimination: ¬E m, n")


    def test_verify_implies_intro(self):
        """
        Test that the function verify_implies_intro is working properly
        TODO: Verify that it is legal to reference the line number
        """
        # Test with valid input
        line1 = ProofLine(1, 'A', 'Assumption')
        line2 = ProofLine(2, 'B', 'Assumption')
        line3 = ProofLine(3, 'A→B', '→I 1-2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_implies_intro(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test with invalid implication
        line1 = ProofLine(1, 'A', 'Assumption')
        line2 = ProofLine(2, 'B', 'Assumption')
        line3 = ProofLine(3, 'A→C', '→I 1-2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_implies_intro(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'The expressions on lines 1 and 2 do not match the implication on line 3')

        # Test with improper line specification
        line1 = ProofLine(1, 'A', 'Assumption')
        line2 = ProofLine(2, 'B', 'Assumption')
        line3 = ProofLine(3, 'A→B', '→I 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_implies_intro(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'Line numbers are not specified correctly.  Conditional Introduction: →I m-n')

    def test_verify_implies_elim(self):
        """
        Test that the function verify_implies_elim is working properly
        """
        # Test with valid input
        line1 = ProofLine(1, 'A→B', 'Premise')
        line2 = ProofLine(2, 'A', 'Premise')
        line3 = ProofLine(3, 'B', '→E 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_implies_elim(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test with invalid elimination
        line1 = ProofLine(1, 'A→B', 'Premise')
        line2 = ProofLine(2, 'A', 'Premise')
        line3 = ProofLine(3, 'C', '→E 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_implies_elim(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'The expressions on lines 2 and 3 do not match the implication on line 1')

        # Test with improper line specification
        line1 = ProofLine(1, 'A→B', 'Premise')
        line2 = ProofLine(2, 'A', 'Premise')
        line3 = ProofLine(3, 'B', '→E 1')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_implies_elim(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, 'Line numbers are not specified correctly.  Conditional Elimination (Modus Ponens): →E m, n')

    def test_verify_indirect_proof(self):
        """
        Test that the function verify_indirect_proof is working properly
        """
        # Test with valid input
        line1 = ProofLine(1, '¬A', 'Premise')
        line2 = ProofLine(2, '⊥', 'Premise')
        line3 = ProofLine(3, 'A', 'IP 1-2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_indirect_proof(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test without contradition
        line1 = ProofLine(1, '¬A', 'Premise')
        line2 = ProofLine(2, 'B', 'Premise')
        line3 = ProofLine(3, 'A', 'IP 1-2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_indirect_proof(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line 2 should be '⊥' (Contradiction)")

        # Test with improper negation
        line1 = ProofLine(1, '¬A', 'Premise')
        line2 = ProofLine(2, '⊥', 'Premise')
        line3 = ProofLine(3, 'B', 'IP 1-2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_indirect_proof(line3, proof)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.err_msg, "Line 1 is not the negation of line 3")

    def test_verify_rule(self):
        """
        Test that the verify_rule function is working properly
        """
        # Test and_intro
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, 'B', 'Premise')
        line3 = ProofLine(3, 'A∧B', '∧I 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_rule(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test and_elim
        line1 = ProofLine(1, 'A∧B', 'Premise')
        line2 = ProofLine(2, 'A', '∧E 1')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_rule(line2, proof)
        self.assertEqual(result.is_valid, True)

        # Test or_intro
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, 'A∨B', '∨I 1')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_rule(line2, proof)
        self.assertEqual(result.is_valid, True)

        # Test or_elim
        line1 = ProofLine(1, 'A∨B', 'Premise')
        line2 = ProofLine(2, 'A', 'Assumption')
        line3 = ProofLine(3, 'C', 'Assumption')
        line4 = ProofLine(4, 'B', 'Assumption')
        line5 = ProofLine(5, 'C', 'Assumption')
        line6 = ProofLine(6, 'C', '∨E 1, 2-3, 4-5')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = verify_rule(line6, proof)
        self.assertEqual(result.is_valid, True)

        # Test not_intro
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, '⊥', 'Premise')
        line3 = ProofLine(3, '¬A', '¬I 1-2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_rule(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test not_elim
        line1 = ProofLine(1, '¬A', 'Premise')
        line2 = ProofLine(2, 'A', 'Premise')
        line3 = ProofLine(3, '⊥', '¬E 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_rule(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test implies_intro
        line1 = ProofLine(1, 'A', 'Assumption')
        line2 = ProofLine(2, 'B', 'Assumption')
        line3 = ProofLine(3, 'A→B', '→I 1-2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_rule(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test implies_elim
        line1 = ProofLine(1, 'A→B', 'Premise')
        line2 = ProofLine(2, 'A', 'Premise')
        line3 = ProofLine(3, 'B', '→E 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_rule(line3, proof)
        self.assertEqual(result.is_valid, True)

        # Test indirect_proof
        line1 = ProofLine(1, '¬A', 'Premise')
        line2 = ProofLine(2, '⊥', 'Premise')
        line3 = ProofLine(3, 'A', 'IP 1-2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_rule(line3, proof)
        self.assertEqual(result.is_valid, True)

    def test_verify_proof(self):
        """
        Test that the verify_proof function is working properly
        """
        # Test and_intro
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, 'B', 'Premise')
        line3 = ProofLine(3, 'A∧B', '∧I 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, True)

        # Test and_elim
        line1 = ProofLine(1, 'A∧B', 'Premise')
        line2 = ProofLine(2, 'A', '∧E 1')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, True)

        # Test or_intro
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, 'A∨B', '∨I 1')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, True)

        # Test or_elim
        line1 = ProofLine(1, 'A∨B', 'Premise')
        line2 = ProofLine(2, 'A', 'Assumption')
        line3 = ProofLine(3, 'C', 'Assumption')
        line4 = ProofLine(4, 'B', 'Assumption')
        line5 = ProofLine(5, 'C', 'Assumption')
        line6 = ProofLine(6, 'C', '∨E 1, 2-3, 4-5')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3, line4, line5, line6])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, True)

        # Test not_intro
        line1 = ProofLine(1, 'A', 'Premise')
        line2 = ProofLine(2, '⊥', 'Premise')
        line3 = ProofLine(3, '¬A', '¬I 1-2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, True)

        # Test not_elim
        line1 = ProofLine(1, '¬A', 'Premise')
        line2 = ProofLine(2, 'A', 'Premise')
        line3 = ProofLine(3, '⊥', '¬E 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, True)

        # Test implies_intro
        line1 = ProofLine(1, 'A', 'Assumption')
        line2 = ProofLine(2, 'B', 'Assumption')
        line3 = ProofLine(3, 'A→B', '→I 1-2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, True)

        # Test implies_elim
        line1 = ProofLine(1, 'A→B', 'Premise')
        line2 = ProofLine(2, 'A', 'Premise')
        line3 = ProofLine(3, 'B', '→E 1, 2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, True)

        # Test indirect_proof
        line1 = ProofLine(1, '¬A', 'Premise')
        line2 = ProofLine(2, '⊥', 'Premise')
        line3 = ProofLine(3, 'A', 'IP 1-2')
        proof = Proof(lines=[])
        proof.lines.extend([line1, line2, line3])
        result = verify_proof(proof)
        self.assertEqual(result.is_valid, True)

class SyntaxTests(TestCase):

    def test_remove_justification_with_just(self):
        """
        remove_justification() should return the substring before the '#'
        """
        str = 'A∧B #∧I, 1,2'
        str2 = Syntax.remove_justification(str)
        self.assertEqual(str2, 'A∧B ')

    def test_remove_justification_without_just(self):
        """
        remove_justification should return the same string if there is no '#'
        """
        str = '(A∧B)∨C'
        str2 = Syntax.remove_justification(str)
        self.assertEqual(str2, '(A∧B)∨C')

    def test_has_valid_symbols_with_valid_symbols(self):
        """
        has_valid_symbols() should return True if all
        characters in the string are valid TFL symbols
        """
        str = '(A∧B)∨C'
        self.assertIs(Syntax.has_valid_symbols(str), True)

    def test_has_valid_symbols_with_invalid_symbols(self):
        """
        has_valid_symbols should return False if one or more
        characters in the string are not valid TFL symbols
        """
        str = 'A>B=C'
        self.assertIs(Syntax.has_valid_symbols(str), False)

    def test_has_balanced_parens_with_balanced_parens(self):
        """
        has_balanced_parens should return True if all parentheses
        in the string are balanced and properly matching
        """
        str = '{[]{()}}'
        self.assertIs(Syntax.has_balanced_parens(str), True)

    def test_has_balanced_parens_with_unbalanced_parens(self):
        """
        has_balanced_parens should return False if parentheses
        in the string are unbalanced or not properly matching
        """
        str = '[{}{})(]'
        str2 = '((()'
        str3 = '(]'
        self.assertIs(Syntax.has_balanced_parens(str), False)
        self.assertIs(Syntax.has_balanced_parens(str2), False)
        self.assertIs(Syntax.has_balanced_parens(str3), False)

    def test_set_depth_array(self):
        str = '(A∧B)∨C'
        str2 = '[(A∧B)∨C]'
        depth_array = Syntax.set_depth_array(str)
        depth_array_2 = Syntax.set_depth_array(str2)
        self.assertEqual(depth_array, [1, 1, 1, 1, 0, 0, 0])
        self.assertEqual(depth_array_2, [1, 2, 2, 2, 2, 1, 1, 1, 0])

    def test_find_main_operator_without_outer_parens(self):
        """
        find_main_operator should return the main logical operator
        of a TFL statement
        """
        str = '(A∧B)∨C'
        self.assertEqual(Syntax.find_main_operator(str), 5)

    def test_find_main_operator_without_outer_parens(self):
        """
        find_main_operator should return the main logical operator
        of a TFL statement
        """
        str = '[(A∧B)∨C]'
        self.assertEqual(Syntax.find_main_operator(str), 6)

    # TODO: Tests for standard order of operations
    # e.g. ¬A∨B should recognize ∨ as the main logical operator    
    # def test_find_main_operator_order_of_operations(self):
    #     """
    #     find_main_operator should apply the order of operations
    #     when multiple logical operators exist at the same depth
    #     """
    #     str = '¬A∨B'
    #     self.assertEqual(Syntax.find_main_operator(str), 2)

    def test_is_valid_TFL_with_atomic_sentence(self):
        """
        is_valid_TFL should return true if provided an atomic sentence
        """
        str1 = 'A'
        str2 = 'Z'
        self.assertIs(Syntax.is_valid_TFL(str1), True)
        self.assertIs(Syntax.is_valid_TFL(str2), True)

    def test_is_valid_TFL_with_one_operator(self):
        """
        is_valid_TFL should return true if provided a well-formed formula (WFF)
        with one operator
        """
        str1 = 'A∧B'
        str2 = '(C∨D)'
        str3 = '¬E'
        str4 = '{X→Y}'
        str5 = 'A↔Z'
        self.assertIs(Syntax.is_valid_TFL(str1), True)
        self.assertIs(Syntax.is_valid_TFL(str2), True)
        self.assertIs(Syntax.is_valid_TFL(str3), True)
        self.assertIs(Syntax.is_valid_TFL(str4), True)
        self.assertIs(Syntax.is_valid_TFL(str5), True)

    def test_is_valid_TFL_with_multiple_operators(self):
        """
        is_valid_TFL should return true if provided a WFF with multiple operators
        """
        str1 = '(A∧B)∨C'
        str2 = '(A∧B)∨[(¬C→D)∧(A↔Z)]'
        self.assertIs(Syntax.is_valid_TFL(str1), True)
        self.assertIs(Syntax.is_valid_TFL(str2), True)

    def test_is_valid_TFL_with_invalid_input(self):
        """
        is_valid_TFL should return false if provided with a string that
        does not conform to TFL sentence rules
        """
        invalid_symbols = 'A+Z'
        unbalanced_parens = '[A∧B)]'
        self.assertIs(Syntax.is_valid_TFL(invalid_symbols), False)
        self.assertIs(Syntax.is_valid_TFL(unbalanced_parens), False)

class TflParseTests(TestCase):

    def test_parser_puts_main_op_in_root_node(self):
        """
        The parser should return a binary tree
        with the main operator as the root node
        """
        str1 = '(A∧B)∨C'
        str2 = '(A∨B)∧[(¬C→D)∧(A↔Z)]'
        node1 = yacc.parser.parse(str1)
        node2 = yacc.parser.parse(str2)
        self.assertEqual(node1.value, '∨')
        self.assertEqual(node2.value, '∧')