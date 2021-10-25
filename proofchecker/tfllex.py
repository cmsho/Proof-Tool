import ply.lex as lex

# List of token names
tokens = [
    'VAR',
    'BOOL',
    'AND',
    'OR',
    'NOT',
    'IMPLIES',
    'IFF',
    'LPAREN',
    'RPAREN',
]

# Regular expression rules for simple tokens
t_VAR=r'[A-Z]'
t_BOOL=r'((True)|(False)|(TRUE)|(FALSE))'
t_AND=r'(∧|\^|\&)'
t_OR=r'(∨|v)'
t_NOT=r'(¬|~|-)'
t_IMPLIES=r'(→|>|(->))'
t_IFF=r'(↔|(<->))'
t_LPAREN=r'((\()|(\[)|(\{))'
t_RPAREN=r'((\))|(\])|(\}))'

# Regular expression rules with action code
# def t_VAR(t):
#     r'[A-Z]'
#     t.value = True
#     return t

# def t_BOOL(t):
#     r'((True)|(TRUE)|(False)|(FALSE))'
#     if t.value == ('True' or 'TRUE'):
#         t.value = True
#     else:
#         t.value = False
#     return t

# TODO: Rewrite this rule so line numbers correspond to ProofLines
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# TODO: Rewrite this to return appropriate respond to client and break 
# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# EOF handling rule
# def t_eof(t):
    # # Get more input (Example)
    # more = input('... ')
    # if more:
    #     self.lexer.input(more)
    #     return self.lexer.token()
    # return None

# Build the lexer
lexer = lex.lex()

# Test it output
def test(data):
    lexer.input(data)
    while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)