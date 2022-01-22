from proofchecker.utils.ply.lex import lexer
from proofchecker.utils.ply import yacc

from .follexer import tokens

precedence = (
    ('right', 'IMPLIES', 'IFF'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)


### From TFL Parser:

# def p_sentence_binary_op(p):
#     '''
#     sentence : sentence IFF sentence
#              | sentence IMPLIES sentence
#              | sentence OR sentence
#              | sentence AND sentence
#     '''

# def p_sentence_unary_op(p):
#     'sentence : NOT sentence'

# def p_sentence_parens(p):
#     'sentence : LPAREN sentence RPAREN'

# def p_sentence(p):
#     '''
#     sentence : BOOL
#              | VAR
#     '''