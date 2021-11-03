from .ply import lex

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
t_BOOL=r'((True)|(TRUE)|(False)|(FALSE)|⊥)'
t_AND=r'(∧|\^|\&)'
t_OR=r'(∨|v)'
t_NOT=r'(¬|~|-)'
t_IMPLIES=r'(→|>|(->))'
t_IFF=r'(↔|(<->))'
t_LPAREN=r'((\()|(\[)|(\{))'
t_RPAREN=r'((\))|(\])|(\}))'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

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