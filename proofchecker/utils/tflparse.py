import ply.yacc as yacc 

from binarytree import Node
from tfllex import tokens

# Ordered lowest to highest
precedence = (
    ('right', 'IMPLIES', 'IFF'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)

def p_sentence_binary_op(p):
    '''
    sentence : sentence IFF sentence
             | sentence IMPLIES sentence
             | sentence OR sentence
             | sentence AND sentence
    '''
    p[0] = Node(p[2])
    p[0].left = p[1]
    p[0].right = p[3]

def p_sentence_unary_op(p):
    'sentence : NOT sentence'
    p[0] = Node(p[1])
    p[0].right = p[2]


def p_sentence_parens(p):
    'sentence : LPAREN sentence RPAREN'
    p[0] = p[2]

def p_sentence(p):
    '''
    sentence : BOOL
             | VAR
    '''
    p[0] = Node(p[1])

# TODO: Create more elegant error handling
#       Define additional grammar rules for errors
# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc(debug=True)

def test():
    while True:
        try:
            s = input('TFL > ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)