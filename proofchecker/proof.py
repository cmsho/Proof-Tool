from .utils import tflparse as yacc
from .utils.binarytree import Node

class Proof:
    
    def __init__(self, lines=[]):
        self.lines = lines
    
    def __str__(self):
        result = ''
        for line in self.lines:
            result += str(line) +'\n'
        return result

class ProofLine:

    def __init__(self, line_no=None, expression=None, rule=None):
        self.line_no = line_no
        self.expression = expression
        self.rule = rule
    
    def __str__(self):
        return ('Line {}: {}, {}'.format(
            self.line_no,
            self.expression,
            self.rule
        ))

class ProofResponse:

    def __init__(self, is_valid=False, err_msg=None):
        self.is_valid = is_valid
        self.err_msg = err_msg


def verify_proof(proof: Proof):
    """
    Verify if a proof is valid, line by line.  
    Returns a ProofResponse, which contains an error message if invalid
    """
    response = ProofResponse()

    # Check each line to determine if it is valid
    for line in proof.lines:
        response = verify_rule(line, proof)

        # If the line is invalid, return the response
        if not response.is_valid:
            return response

    # If all lines are valid, proof is valid
    response.is_valid = True
    return response


def verify_rule(current_line: ProofLine, proof: Proof):
    """
    Determines what rule is being applied, then calls the appropriate
    function to verify the rule is applied correctly
    """
    rule = current_line.rule

    if rule.casefold() == 'premise':
        # TODO: Verify premise
        return ProofResponse(is_valid=True)
    elif rule.casefold() == ('assumption' or 'assumpt'):
        # TODO: Verify assumption
        return ProofResponse(is_valid=True)
    elif rule.casefold() == 'x':
        # TODO: Verify explosion
        return ProofResponse(is_valid=True)
    else:
        rule_type = rule[0:2]
        match rule_type:
            case '∧I':
                return verify_and_intro(current_line, proof)
            case '∧E':
                return verify_and_elim(current_line, proof)
            case '∨I':
                return verify_or_intro(current_line, proof)
            case '∨E':
                return verify_or_elim(current_line, proof)
            case '¬I':
                return verify_not_intro(current_line, proof)
            case '¬E':
                return verify_not_elim(current_line, proof)
            case '→I':
                return verify_implies_intro(current_line, proof)
            case '→E':
                return verify_implies_elim(current_line, proof)
            case 'IP':
                return verify_indirect_proof(current_line, proof)
    
    # If we reach this point, rule cannot be determined
    response = ProofResponse()
    response.err_msg = "Rule on line {} cannot be determined"\
        .format(str(current_line.line_no))
    return response

def make_tree(string: str):
    """
    Function to construct a binary tree
    """
    return yacc.parser.parse(string)

def find_line(rule: str):
    """
    Find a single line from a TFL rule
    """
    target_line = rule[3:len(rule)]
    target_line = target_line.strip()
    return target_line

def find_lines(rule: str):
    """
    Find multiple lines from a TFL rule
    """
    target_lines = rule[3:len(rule)]
    target_lines = target_lines.replace('-', ' ')
    target_lines = target_lines.replace(',', '')
    target_lines = target_lines.split()
    return target_lines

def find_expression(target_line: int, proof: Proof):
    """
    Find the expression on line (m) of a Proof
    """
    expression = None
    for line in proof.lines:
        if float(target_line) == float(line.line_no):
            expression = line.expression
            break
    return expression

def find_expressions(target_lines: list[int], proof: Proof):
    """
    Find the expressions on lines (m, n) of a Proof
    """
    expressions = []
    for num in target_lines:
        for line in proof.lines:
            if float(num) == float(line.line_no):
                expressions.append(line.expression)
                break
    return expressions

def verify_and_intro(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule ∧I m, n
    (Conjunction Introduction)
    """
    rule = current_line.rule
    response = ProofResponse()

    # Attempt to find lines (m, n) 
    try:
        target_lines = find_lines(rule)

        # Search for lines (m, n) in the proof
        try:
            expressions = find_expressions(target_lines, proof)
            
            # Join the two expressions in a tree
            root_m_and_n = Node('∧')
            root_m_and_n.left = make_tree(expressions[0])
            root_m_and_n.right = make_tree(expressions[1])

            root_n_and_m = Node('∧')
            root_n_and_m.left = make_tree(expressions[1])
            root_n_and_m.right = make_tree(expressions[0])

            # Create a tree from the current expression
            root_current = make_tree(current_line.expression)

            # Compare the trees
            if root_current == (root_m_and_n or root_n_and_m):
                response.is_valid = True
                return response
            else:
                response.err_msg = "The conjunction of lines {} and {} does not equal line {}"\
                    .format(str(target_lines[0]), str(target_lines[1]), str(current_line.line_no))
                return response
        
        except:
            response.err_msg = "Line numbers are not specified correctly.  Conjunction Introduction: ∧I m, n"
            return response

    except:
        response.err_msg = "Rule is not formatted properly.  Conjunction Introduction: ∧I m, n"
        return response

def verify_and_elim(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule ∧E m
    (Conjunction Elimination)
    """
    rule = current_line.rule
    response = ProofResponse()

    # Attempt to find line m 
    try:
        target_line = find_line(rule)

        # Search for line m in the proof
        try:
            expression = find_expression(target_line, proof)
            
            # Create trees for the left and right side of the target expression
            root_target = make_tree(expression)
            root_left = root_target.left
            root_right = root_target.right

            # Create a tree from the current expression
            root_current = make_tree(current_line.expression)

            # Compare the trees
            if root_current == (root_left or root_right):
                response.is_valid = True
                return response
            else:
                response.err_msg = "Line {} does not follow from line {}"\
                    .format(str(current_line.line_no), str(target_line))
                return response
        
        except:
            response.err_msg = "Line numbers are not specified correctly.  Conjunction Elimination: ∧E m"
            return response      

    except:
        response.err_msg = "Rule not formatted properly.  Conjunction Elimination: ∧E m"
        return response

def verify_or_intro(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule ∨I m
    (Disjunction Introduction)
    """
    rule = current_line.rule
    response = ProofResponse()

    # Attempt to find line m
    try:
        target_line = find_line(rule)

        # Search for line m in the proof
        try:
            expression = find_expression(target_line, proof)

            # Create a tree for the target expression
            root_target = make_tree(expression)

            # Create trees for left and right side of current expression
            root_current = make_tree(current_line.expression)
            root_left = root_current.left
            root_right = root_current.right

            # Compare the trees
            if root_target == (root_left or root_right):
                response.is_valid = True
                return response
            else:
                response.err_msg = "Line {} does not follow from line {}"\
                    .format(str(current_line.line_no), str(target_line))
                return response

        except:
            response.err_msg = "Line numbers are not specified correctly.  Disjunction Introduction: ∨I m"
            return response

    except:
        response.err_msg = "Rule not formatted properly.  Disjunction Introduction: ∨I m"
        return response


def verify_or_elim(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule ∨E m, i-j, k-l
    (Disjunction Elimination)
    """
    rule = current_line.rule
    response = ProofResponse()

    # Attempt to find lines (m, i-j, k-l)
    try:
        target_lines = find_lines(rule)

        # Search for lines m, i-j, k-l in the proof
        try:
            expressions = find_expressions(target_lines, proof)
        
            # Create trees for expressions on lines m, i, j, k, and l
            root_m = make_tree(expressions[0])
            root_i = make_tree(expressions[1])
            root_j = make_tree(expressions[2])
            root_k = make_tree(expressions[3])
            root_l = make_tree(expressions[4])
            root_current = make_tree(current_line.expression)

            # Verify lines i and k represent separate sides of expression m
            if (root_i != root_k):
                if (root_i == root_m.left) or (root_i == root_m.right):
                    if (root_k == root_m.left) or (root_k == root_m.right):
                        # Verify that j, l, and current_line expression are equivalent
                        if (root_j == root_l) and (root_l == root_current):
                            response.is_valid = True
                            return response
                        else:
                            response.err_msg = "The expressions on lines {}, {} and {} are not equivalent"\
                                .format(str(target_lines[2]),str(target_lines[4]),str(current_line.line_no))
                            return response
                    else:
                        response.err_msg = "The expression on line {} is not part of the disjunction on line {}"\
                            .format(str(target_lines[3]),str(target_lines[0]))
                        return response
                else:
                    response.err_msg = "The expression on line {} is not part of the disjunction on line {}"\
                        .format(str(target_lines[1]),str(target_lines[0]))
                    return response          
            else:
                response.err_msg = "The expressions on lines {} and {} should be different"\
                    .format(str(target_lines[1]),str(target_lines[3]))
                return response    
        except:
            response.err_msg = "Line numbers are not specified correctly.  Disjunction Elimination: ∨E m, i-j, k-l"
            return response        
    except:
        response.err_msg = "Rule not formatted properly.  Disjunction Elimination: ∨E m, i-j, k-l"
        return response


def verify_not_intro(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule ¬I m-n
    (Negation Introduction)
    """
    rule = current_line.rule
    response = ProofResponse()

    # Attempt to find lines (i-j)
    try:
        target_lines = find_lines(rule)

        # Search for lines i-j in the proof
        try:
            expressions = find_expressions(target_lines, proof)

            # Create trees from the expressions on lines i-j
            root_i = make_tree(expressions[0])
            root_j = make_tree(expressions[1])

            # Create a tree from the expression on the current_line
            root_current = make_tree(current_line.expression)

            # Verify current line is the negation of line i
            if (root_current.value == '¬') and (root_current.right == root_i):
                
                # TODO: Test this
                if (root_j.value == '⊥') or (root_j.value.casefold() == 'false'):
                    response.is_valid = True
                    return response
                else:
                    response.err_msg = "Line {} should be '⊥' (Contradiction)"\
                        .format(str(target_lines[1]))
                    return response

            else:
                response.err_msg = "Line {} is not the negation of line {}"\
                    .format(str(current_line.line_no),str(target_lines[0]))
                return response

        except:
            response.err_msg = "Line numbers are not specified correctly.  Negation Introduction: ¬I m-n"
            return response        

    except:
        response.err_msg = "Rule not formatted properly.  Negation Introduction: ¬I m-n"
        return response


def verify_not_elim(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule ¬E m, n
    (Negation Elimination)
    """
    rule = current_line.rule
    response = ProofResponse()

    # Attempt to find lines (m, n)
    try:
        target_lines = find_lines(rule)

        # Search for lines (m, n) in the proof
        try:
            expressions = find_expressions(target_lines, proof)

            # Create trees from the expressions on lines (m, n)
            root_m = make_tree(expressions[0])
            root_n = make_tree(expressions[1])

            # Create a tree from the expression on the current_line
            root_current = make_tree(current_line.expression)

            # Verify m is the negation of n
            if (root_m.value == '¬') and (root_m.right == root_n):
                
                # TODO: Test this
                if (root_current.value == '⊥') or (root_current.value.casefold() == 'false'):
                    response.is_valid = True
                    return response
                else:
                    response.err_msg = "Line {} should be '⊥' (Contradiction)"\
                        .format(str(current_line.line_no))
                    return response

            else:
                response.err_msg = "Line {} is not the negation of line {}"\
                    .format(str(target_lines[0]),str(target_lines[1]))
                return response

        except:
            response.err_msg = "Line numbers are not specified correctly.  Negation Elimination: ¬E m, n"
            return response        

    except:
        response.err_msg = "Rule not formatted properly.  Negation Elimination: ¬E m, n"
        return response


def verify_implies_intro(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule →I m-n
    (Conditional Introduction)
    TODO: Verify that it is legal to reference the line numbers
    """
    rule = current_line.rule
    response = ProofResponse()

    # Attempt to find lines m-n
    try:
        target_lines = find_lines(rule)
        
        # Search for lines m-n in the proof
        try:
            expressions = find_expressions(target_lines, proof)

            root_m = make_tree(expressions[0])
            root_n = make_tree(expressions[1])
            root_current = make_tree(current_line.expression)

            if (root_current.left == root_m) and (root_current.right == root_n):
                response.is_valid = True
                return response
            else:
                response.err_msg = "The expressions on lines {} and {} do not match the implication on line {}"\
                    .format(str(target_lines[0]),str(target_lines[1]),str(current_line.line_no))
                return response

        except:
            response.err_msg = "Line numbers are not specified correctly.  Conditional Introduction: →I m-n"
            return response

    except:
        print("Rule not formatted properly.  Conditional Introduction: →I m-n")
        return response


def verify_implies_elim(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule →E m, n
    (Conditional Elimination (Modus Ponens))
    """
    rule = current_line.rule
    response = ProofResponse()

    # Attempt to find lines (m, n) 
    try:
        target_lines = find_lines(rule)

        # Search for lines (m, n) in the proof
        try:
            expressions = find_expressions(target_lines, proof)
            
            root_implies = make_tree(expressions[0])

            root_combined = Node('→')
            root_combined.left = make_tree(expressions[1])
            root_combined.right = make_tree(current_line.expression)

            # Compare the trees
            if root_implies == root_combined:
                response.is_valid = True
                return response
            else:
                response.err_msg = "The expressions on lines {} and {} do not match the implication on line {}"\
                    .format(str(target_lines[1]),str(current_line.line_no),str(target_lines[0]))
                return response
        
        except:
            response.err_msg = "Line numbers are not specified correctly.  Conditional Elimination (Modus Ponens): →E m, n"
            return response

    except:
        response.err_msg = "Rule not formatted properly.  Conditional Elimination (Modus Ponens): →E m, n"
        return response


def verify_indirect_proof(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule IP i-j
    (Indirect Proof)
    """
    rule = current_line.rule
    response = ProofResponse()

    # Attempt to find lines i-j
    try:
        target_lines = find_lines(rule)

        # Search for lines i-j in the proof
        try:
            expressions = find_expressions(target_lines, proof)

            # Create trees from the expressions on lines i-j
            root_i = make_tree(expressions[0])
            root_j = make_tree(expressions[1])

            # Create a tree from the expression on the current_line
            root_current = make_tree(current_line.expression)

            # Verify line i is the negation of current line
            if (root_i.value == '¬') and (root_i.right == root_current):
                
                # TODO: Test this
                if (root_j.value == '⊥') or (root_j.value.casefold() == 'false'):
                    response.is_valid = True
                    return response
                else:
                    response.err_msg = "Line {} should be '⊥' (Contradiction)"\
                        .format(str(target_lines[1]))
                    return response

            else:
                response.err_msg = "Line {} is not the negation of line {}"\
                    .format(str(target_lines[0]),str(current_line.line_no))
                return response

        except:
            response.err_msg = "Line numbers are not specified correctly.  Indirect Proof: IP i-j"
            return response        

    except:
        response.err_msg = "Rule not formatted properly.  Indirect Proof: IP i-j"
        return response