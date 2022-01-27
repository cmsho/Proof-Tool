from django.test import TestCase
from proofchecker.utils import folparser
from proofchecker.utils.follexer import IllegalCharacterFOLError, lexer


class FOLLexerTests(TestCase):
    def test_lexer_raises_IllegalCharacterError(self):
        """
        The lexer should raise an IllegalCharacterError
        if provided an invalid character
        """
        self.assertRaises(IllegalCharacterFOLError, folparser.parser.parse, 'A1', lexer=lexer)


class FOLParserTests(TestCase):
    def test_parser(self):
        """
        The parser should create a binary tree representing the FOL expression
        """
        str1 = 'a=b'
        str2 = 'F(x)'
        str3 = 'F(x) ∨ G(y)'
        str4 = '∀x∈S H(x)'
        str5 = 'Fabc'
        str6 = 'Fabc > Gxyz'
        node1 = folparser.parser.parse(str1, lexer=lexer)
        node2 = folparser.parser.parse(str2, lexer=lexer)
        node3 = folparser.parser.parse(str3, lexer=lexer)
        node4 = folparser.parser.parse(str4, lexer=lexer)
        node5 = folparser.parser.parse(str5, lexer=lexer)
        node6 = folparser.parser.parse(str6, lexer=lexer)
        self.assertEqual(node1.value, 'a=b')
        self.assertEqual(node2.value, 'F(x)')
        self.assertEqual(node3.value, '∨')
        self.assertEqual(node3.left.value, 'F(x)')
        self.assertEqual(node3.right.value, 'G(y)')
        self.assertEqual(node4.value, '∀x∈S')
        self.assertEqual(node4.right.value, 'H(x)')
        self.assertEqual(node5.value, 'Fabc')
        self.assertEqual(node6.value, '→')
        self.assertEqual(node6.left.value, 'Fabc')
        self.assertEqual(node6.right.value, 'Gxyz')

    def test_parser_reformatting_symbols(self):
        """
        The parser should reformat symbols as necessary
        """
        str1 = 'F(x)^G(y)'
        str2 = 'A(a)|B(b)'
        str3 = '~H(z)'
        str4 = 'F(x)>G(y)'
        str5 = 'H(a)->J(b)'
        str6 = 'L(i)<->M(j)'
        str7 = 'Q(s)&R(s)'
        node1 = folparser.parser.parse(str1, lexer=lexer)
        node2 = folparser.parser.parse(str2, lexer=lexer)
        node3 = folparser.parser.parse(str3, lexer=lexer)
        node4 = folparser.parser.parse(str4, lexer=lexer)
        node5 = folparser.parser.parse(str5, lexer=lexer)
        node6 = folparser.parser.parse(str6, lexer=lexer)
        node7 = folparser.parser.parse(str7, lexer=lexer)
        self.assertEqual(node1.value, '∧')
        self.assertEqual(node2.value, '∨')
        self.assertEqual(node3.value, '¬')
        self.assertEqual(node4.value, '→')
        self.assertEqual(node5.value, '→')
        self.assertEqual(node6.value, '↔')
        self.assertEqual(node7.value, '∧')

    def test_parser_raises_SyntaxError(self):
        """
        The parser should raise a TFLSyntaxError
        if provided invalid syntax
        """
        str1='A(x)∧B'
        str2='A∧B'
        self.assertRaises(SyntaxError, folparser.parser.parse, str1, lexer=lexer)
        self.assertRaises(SyntaxError, folparser.parser.parse, str2, lexer=lexer)