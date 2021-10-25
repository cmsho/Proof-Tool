import ply.yacc as yacc 

from tfllex import tokens

class Node:
    def __init__(self, data):
        self.left = None
        self.value = data
        self.right = None

# Ordered lowest to highest
precedence = (
    ('right', 'IMPLIES', 'IFF'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)

def p_sentence_binop(p):
    '''
    sentence : sentence IFF sentence
             | sentence IMPLIES sentence
             | sentence OR sentence
             | sentence AND sentence
    '''
    p[0] = Node(p[2])
    p[0].left = p[1]
    p[0].right = p[3]

def p_sentence_monop(p):
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

def preorder(node):
    if node:
        print(node.value)
        preorder(node.left)
        preorder(node.right)

def inorder(node):
    if node:
        inorder(node.left)
        print(node.value)
        inorder(node.right)

def postorder(node):
    if node:
        postorder(node.left)
        postorder(node.right)
        print(node.value)


# First attempts at definitions.  Might throw these out later.

# def p_sentence_iff(p):
#     'sentence : sentence IFF sentence'
#     pass
#     # p[0] = ??

# def p_sentence_implies(p):
#     'sentence : sentence IMPLIES sentence'
#     pass
#     # p[0] = ??
    
# def p_sentence_or(p):
#     'sentence : sentence OR sentence'
#     pass
#     # p[0] = p[1] or p[3]

# def p_sentence_and(p):
#     'sentence : sentence AND sentence'
#     pass
#     # p[0] = p[1] and p[3]

# def p_sentence_not(p):
#     'sentence : NOT sentence'
#     pass
#     # p[0] = not p[1]

# def p_sentence_parens(p):
#     'sentence : LPAREN sentence RPAREN'
#     pass
#     # p[0] = p[2]

# def p_sentence_atomic(p):
#     'sentence : VAR'
#     pass
#     # p[0] = p[1]

# def p_sentence_bool(p):
#     'sentence : BOOL'
#     pass
#     # p[0] = p[1]