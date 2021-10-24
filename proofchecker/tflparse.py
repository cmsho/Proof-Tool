import ply.yacc as yacc 

from tfllex import tokens

# Ordered lowest to highest
precedence = (
    ('right', 'IMPLIES', 'IFF'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)

def p_sentence_iff(p):
    'sentence : sentence IFF sentence'
    pass
    # p[0] = ??

def p_sentence_implies(p):
    'sentence : sentence IMPLIES sentence'
    pass
    # p[0] = ??
    
def p_sentence_or(p):
    'sentence : sentence OR sentence'
    pass
    # p[0] = p[1] or p[3]

def p_sentence_and(p):
    'sentence : sentence AND sentence'
    pass
    # p[0] = p[1] and p[3]

def p_sentence_not(p):
    'sentence : NOT sentence'
    pass
    # p[0] = not p[1]

def p_sentence_parens(p):
    'sentence : LPAREN sentence RPAREN'
    pass
    # p[0] = p[2]

def p_sentence_atomic(p):
    'sentence : VAR'
    pass
    # p[0] = p[1]

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