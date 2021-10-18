from django.test import TestCase

from .syntax import Syntax

# Create your tests here.
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
        in teh string are unbalanced or not properly matching
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
        depthArray = Syntax.set_depth_array(str)
        depthArray2 = Syntax.set_depth_array(str2)
        self.assertEqual(depthArray, [1, 1, 1, 1, 0, 0, 0])
        self.assertEqual(depthArray2, [1, 2, 2, 2, 2, 1, 1, 1, 0])

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
        # str2 = '(A∧B)∨[(¬C→D)∧(A↔Z)'
        self.assertIs(Syntax.is_valid_TFL(str1), True)
        # self.assertIs(Syntax.is_valid_TFL(str2), True)
