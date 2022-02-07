from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.utils import numparser
from proofchecker.utils.constants import Constants
from proofchecker.utils.numlexer import lexer as numlexer
from proofchecker.utils.tfllexer import IllegalCharacterError


# Parsing methods
def depth(line_no):
    """
    Calculates the depth of a line number
    """
    return numparser.parser.parse(line_no, lexer=numlexer)

def make_tree(string: str, parser):
    """
    Function to construct a binary tree
    """
    return parser.parse(string, lexer=parser.lexer)

def is_line_no(string: str):
    """
    Function to determine if a line number is valid
    """
    return numparser.parser.parse(string, lexer=numlexer)

def is_name(ch):
    """
    Function to determine if a character is an FOL name (a-r)
    """
    return (ch in Constants.NAMES)


def is_var(ch):
    """
    Function to determine if a character is an FOL variable (s-z)
    """
    return (ch in Constants.VARS)

def is_predicate(ch):
    """
    Function to determine if a character is an FOL predicate (A-R)
    """
    return (ch in Constants.PREDICATES)

def is_domain(ch):
    """
    Function to determine if a character is an FOL domain (S-Z)
    """
    return (ch in Constants.DOMAINS)

# Proof Verification
def is_conclusion(current_line: ProofLineObj, proof: ProofObj, parser):
    """
    Verify whether the current_line is the desired conclusion
    """
    response = ProofResponse
    try:
        current = make_tree(current_line.expression, parser)
        conclusion = make_tree(proof.conclusion, parser)

        if current == conclusion:
            return True
        
        return False
    except:
        return False

def is_valid_expression(expression: str, parser):
    """
    Verify if a string is a valid Boolean expression
    Returns a Boolean (True/False)
    """
    # Verify the expression is valid

    if expression == "":
        return False
    try:
        expression = make_tree(expression, parser)
        return True
    except:
        return False

def verify_expression(expression: str, parser):
    """
    Verify if a string is a valid boolean expression
    Returns a ProofResponse
    """
    response = ProofResponse()
    if expression == "":
        response.err_msg = "Expression cannot be an empty string"
        return response
    # Verify the expression is valid
    try:
        exp = make_tree(expression, parser)
        response.is_valid = True
        return response

    except IllegalCharacterError as char_err:
        response.err_msg = "{} in expression {}"\
            .format(char_err.message, str(expression))
        return response 
    except:
        response.err_msg = "Syntax error in expression {}"\
            .format(str(expression))
        return response
    

def verify_line_citation(current_line: ProofLineObj, cited_line: ProofLineObj):
    """
    Verify whether an individual line citation is valid
    Returns a ProofResponse with an error message if invalid
    """
    response = ProofResponse()
    
    try:
        # Calculate the depth of each line number
        current_depth = depth(str(current_line.line_no))
        cited_depth = depth(str(cited_line.line_no))

        # Check if the cited line occurs within a subproof that has not been closed
        # before the line where the rule is applied (this is a violation)
        if cited_depth > current_depth:
            response.err_msg = "Line {} occurs within a subproof that has not been closed prior to line {}"\
                .format(str(cited_line.line_no), str(current_line.line_no))
            return response

        # Create an array of nested line numbers
        current_nums = str(current_line.line_no).replace('.', ' ')
        current_nums = current_nums.split()
        cited_nums = str(cited_line.line_no).replace('.', ' ')
        cited_nums = cited_nums.split()
        x = 0
        
        # Check that the current line occurs after the cited line in the proof
        while x < cited_depth:
            if current_nums[x] < cited_nums[x]:
                response.err_msg = "Invalid citation: line {} occurs after line {}"\
                    .format(str(cited_line.line_no), str(current_line.line_no))
                return response
            elif cited_nums[x] < current_nums[x]:
                break
            x += 1
        
        # If all the other checks pass, line citation is valid
        response.is_valid = True
        return response

    except:
        response.err_msg = "Line citations are not formatted properly"
        return response

def verify_subproof_citation(current_line: ProofLineObj, cited_line: ProofLineObj):
    """
    Verify whether an subproof citation is valid
    Returns a ProofResponse with an error message if invalid
    """

    response = ProofResponse()
    
    try:
        # Calculate the depth of each line number
        current_depth = depth(str(current_line.line_no))
        cited_depth = depth(str(cited_line.line_no))-1

        # Check if the cited line occurs within a subproof that has not been closed
        # before the line where the rule is applied (this is a violation)
        if cited_depth > current_depth:
            response.err_msg = "Line {} occurs within a subproof that has not been closed prior to line {}"\
                .format(str(cited_line.line_no), str(current_line.line_no))
            return response

        # Create an array of nested line numbers
        current_nums = str(current_line.line_no).replace('.', ' ')
        current_nums = current_nums.split()
        cited_nums = str(cited_line.line_no).replace('.', ' ')
        cited_nums = cited_nums.split()
        x = 0
        
        # Check that the current line occurs after the cited line in the proof
        while x < cited_depth:
            if current_nums[x] < cited_nums[x]:
                response.err_msg = "Invalid citation: line {} occurs after line {}"\
                    .format(str(cited_line.line_no), str(current_line.line_no))
                return response
            elif cited_nums[x] < current_nums[x]:
                break
            x += 1
        
        # If all the other checks pass, line citation is valid
        response.is_valid = True
        return response

    except:
        response.err_msg = "Line numbers are not formatted properly"
        return response

def get_premises(premises: str):
    """
    Take a string of comma separated-premises
    and return an array of premises
    """
    if premises == None:
        return ''
    premises = premises.replace(' ', '')
    premises = premises.replace(';', ' ')
    return premises.split()

def get_line_no(rule):
    """
    Get a single line number in a TFL citation
    """
    target_line_no = rule[2:len(rule)]
    return target_line_no.strip()

def get_line_nos(rule):
    """
    Get multiple line numbers in a TFL citation
    """
    target_line_nos = rule[3:len(rule)]
    target_line_nos = target_line_nos.replace('-', ' ')
    target_line_nos = target_line_nos.replace(',', ' ')
    return target_line_nos.split()

def get_line(rule: str, proof: ProofObj):
    """
    Find a single line from a TFL rule
    """
    target_line_no = get_line_no(rule)
    target_line = None
    for line in proof.lines:
        if str(target_line_no) == str(line.line_no):
            target_line = line
            break
    return target_line

def get_line_with_line_no(line_no: str, proof: ProofObj):
    """
    Find a single line using the line number
    """
    target_line = None
    for line in proof.lines:
        if line_no == str(line.line_no):
            target_line = line
            break
    return target_line    

def get_line_DNE(rule: str, proof: ProofObj):
    """
    Find a single line for rule DNE
    """
    target_line_no = rule[3:len(rule)].strip()
    target_line = None
    for line in proof.lines:
        if str(target_line_no) == str(line.line_no):
            target_line = line
            break
    return target_line

def get_lines(rule: str, proof: ProofObj):
    """
    Find multiple lines from a TFL rule
    """
    target_line_nos = get_line_nos(rule)
    target_lines = []
    for num in target_line_nos:
        for line in proof.lines:
            if str(num) == str(line.line_no):
                target_lines.append(line)
                break
    return target_lines

def get_lines_in_subproof(line_no: str, proof: ProofObj):
    """
    Returns the first and last line of a subproof
    """
    subproof = []
    for line in proof:
        if line.line_no.startswith(line_no):
            subproof.append(line)
    if len(subproof) > 1:
        return[subproof[0], subproof[len(subproof)-1]]
    else:
        return None

def get_expressions(lines):
    """
    Returns an array of expressions from an array of ProofLines
    """
    expressions = []
    for line in lines:
        expressions.append(line.expression)
    return expressions

def clean_rule(rule: str):
    """
    Replace symbols to clean the rule for rule verification
    """
    if rule[0] in '^&':
        clean_rule = '∧' + rule[1:len(rule)]
        return clean_rule
    if rule[0] == 'v':
        clean_rule = '∨' + rule[1:len(rule)]
        return clean_rule
    if rule[0] == '>':
        clean_rule = '→' + rule[1:len(rule)]
        return clean_rule
    if rule[0:2] == '->':
        clean_rule = '→' + rule[2:len(rule)]
        return clean_rule
    if rule[0] in '~-':
        clean_rule = '¬' + rule[1:len(rule)]
        return clean_rule

    return rule