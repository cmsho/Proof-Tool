from proofchecker.utils.tfllex import IllegalCharacterError
from .utils import tflparse, numparse
from .utils.tfllex import lexer as tfllexer
from .utils.numlex import lexer as numlexer
from .utils.binarytree import Node

class Proof:
    
    def __init__(self, premises=[], conclusion='', lines=[], created_by=''):
        self.premises = premises
        self.conclusion = conclusion
        self.lines = lines
        self.created_by = created_by
    
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

    for line in proof.lines:

        # Verify the line has a line number
        if not line.line_no:
            response.err_msg = "One or more lines is missing a line number"
            return response

        # Verify the expression is valid
        try:
            expression = make_tree(line.expression)
            if expression == None:
                response.err_msg = "No expression on line {}"\
                    .format(str(line.line_no))
                return response
        except IllegalCharacterError as char_err:
            response.err_msg = "{} on line {}"\
                .format(char_err.message, str(line.line_no))
            return response 
        except:
            response.err_msg = "Syntax error on line {}"\
                .format(str(line.line_no))
            return response
        
        # Verify the rule is valid
        response = verify_rule(line, proof)
        if not response.is_valid:
            return response

    last_line = proof.lines[len(proof.lines)-1]
    conclusion = is_conclusion(last_line, proof)
    response.is_valid = True

    # If the last line is the desired conclusion, it is a full and complete proof
    if conclusion:
        return response

    # If not, the proof is incomplete
    else:
        response.err_msg = "All lines are valid, but the proof is incomplete"
        return response


def verify_rule(current_line: ProofLine, proof: Proof):
    """
    Determines what rule is being applied, then calls the appropriate
    function to verify the rule is applied correctly
    """
    rule = current_line.rule

    if rule.casefold() == 'premise':
        return verify_premise(current_line, proof)
    elif rule.casefold() == ('assumption' or 'assumpt'):
        return verify_assumption(current_line)
    elif rule.casefold() == 'x':
        return verify_explosion(current_line, proof)
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

def depth(line_no):
    """
    Calculates the depth of a line number
    """
    return numparse.parser.parse(line_no, lexer=numlexer)

def verify_citation(current_line: ProofLine, cited_line: ProofLine):
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
        response.err_msg = "Line numbers are not formatted properly"
        return response


def make_tree(string: str):
    """
    Function to construct a binary tree
    """
    return tflparse.parser.parse(string, lexer=tfllexer)

def is_conclusion(current_line: ProofLine, proof: Proof):
    """
    Verify whether the current_line is the desired conclusion
    """
    response = ProofResponse
    try:
        current = make_tree(current_line.expression)
        conclusion = make_tree(proof.conclusion)

        if current == conclusion:
            return True
        
        return False
    except:
        return False

def find_line(rule: str, proof: Proof):
    """
    Find a single line from a TFL rule
    """
    target_line_no = rule[3:len(rule)]
    target_line_no = target_line_no.strip()
    target_line = None
    for line in proof.lines:
        if str(target_line_no) == str(line.line_no):
            target_line = line
            break
    return target_line

def find_line_explosion(rule: str, proof: Proof):
    """
    Find a single line from the TFL rule explosion
    """
    target_line_no = rule[2:len(rule)]
    target_line_no = target_line_no.strip()
    target_line = None
    for line in proof.lines:
        if str(target_line_no) == str(line.line_no):
            target_line = line
            break
    return target_line

def find_lines(rule: str, proof: Proof):
    """
    Find multiple lines from a TFL rule
    """
    target_line_nos = rule[3:len(rule)]
    target_line_nos = target_line_nos.replace('-', ' ')
    target_line_nos = target_line_nos.replace(',', '')
    target_line_nos = target_line_nos.split()
    target_lines = []
    for num in target_line_nos:
        for line in proof.lines:
            if str(num) == str(line.line_no):
                target_lines.append(line)
                break
    return target_lines

def find_expressions(lines):
    """
    Returns an array of expressions from an array of ProofLines
    """
    expressions = []
    for line in lines:
        expressions.append(line.expression)
    return expressions

def verify_premise(current_line: ProofLine, proof: Proof):
    """
    Verify that "premise" is valid justification for a line
    """
    response = ProofResponse()
    try:
        current_exp = current_line.expression
        current = make_tree(current_exp)

        # If there is only one premise
        if isinstance(proof.premises, str):
            if make_tree(proof.premises) == current:
                response.is_valid = True
                return response
            else:
                response.err_msg = "Expression on line {} is not a premise"\
                    .format(str(current_line.line_no))
                return response                

        # If multiple expressions, search for the premise
        for premise in proof.premises:
            if make_tree(premise) == current:
                response.is_valid = True
                return response
    
        # If not found, invalid
        response.err_msg = "Expression on line {} not found in premises"\
            .format(str(current_line.line_no))
        return response

    except:
        response.err_msg = "One or more premises is invalid"
        return response

def verify_assumption(current_line: ProofLine):
    """
    Verify that an assumption is valid
    """
    response = ProofResponse()

    try:
        nums = str(current_line.line_no).replace('.', ' ')
        nums = nums.split()
        last_num = nums[len(nums)-1]

        # Assumptions should start a new subproof
        # (i.e. the last number in the line number should be '1')
        if str(last_num) == '1':
            response.is_valid = True
            return response
    
        response.err_msg = 'Assumptions can only exist at the start of a subproof'
        return response

    except:
        response.err_msg = 'One or more invalid line numbers.'
        return response

def verify_explosion(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule X m
    (Explosion)
    """
    rule = current_line.rule
    response = ProofResponse()

    # Attempt to find line m
    try:
        target_line = find_line_explosion(rule, proof)

        # Verify if line citation is valid
        result = verify_citation(current_line, target_line)
        if result.is_valid == False:
            return result

        try: 
            expression = target_line.expression
            root = make_tree(expression)

            # Verify line j is a contradiction
            if (root.value == '⊥') or (root.value.casefold() == 'false'):
                response.is_valid = True
                return response
            else:
                response.err_msg = "Line {} should be '⊥' (Contradiction)"\
                    .format(str(target_line.line_no))
                return response

        except:
            response.err_msg = "Line numbers are not specified correctly.  Explosion: X m"
            return response      

    except:
        response.err_msg = "Rule not formatted properly.  Conjunction Elimination: X m"
        return response 

def verify_and_intro(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule ∧I m, n
    (Conjunction Introduction)
    """
    rule = current_line.rule
    response = ProofResponse()

    # Attempt to find lines (m, n) 
    try:
        target_lines = find_lines(rule, proof)

        for line in target_lines:
            result = verify_citation(current_line, line)
            if result.is_valid == False:
                return result

        # Search for lines (m, n) in the proof
        try:
            expressions = find_expressions(target_lines)
            
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
                    .format(str(target_lines[0].line_no), str(target_lines[1].line_no), str(current_line.line_no))
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
        target_line = find_line(rule, proof)

        # Verify if line citation is valid
        result = verify_citation(current_line, target_line)
        if result.is_valid == False:
            return result

        # Search for line m in the proof
        try:
            expression = target_line.expression
            
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
                    .format(str(current_line.line_no), str(target_line.line_no))
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
        target_line = find_line(rule, proof)

        # Verify if line citation is valid
        result = verify_citation(current_line, target_line)
        if result.is_valid == False:
            return result

        # Search for line m in the proof
        try:
            expression = target_line.expression

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
                    .format(str(current_line.line_no), str(target_line.line_no))
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
        target_lines = find_lines(rule, proof)

        # Verify that line citations are valid
        for line in target_lines:
            result = verify_citation(current_line, line)
            if result.is_valid == False:
                return result

        # Search for lines m, i-j, k-l in the proof
        try:
            expressions = find_expressions(target_lines)
        
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
                                .format(str(target_lines[2].line_no),str(target_lines[4].line_no),str(current_line.line_no))
                            return response
                    else:
                        response.err_msg = "The expression on line {} is not part of the disjunction on line {}"\
                            .format(str(target_lines[3].line_no),str(target_lines[0].line_no))
                        return response
                else:
                    response.err_msg = "The expression on line {} is not part of the disjunction on line {}"\
                        .format(str(target_lines[1].line_no),str(target_lines[0].line_no))
                    return response          
            else:
                response.err_msg = "The expressions on lines {} and {} should be different"\
                    .format(str(target_lines[1].line_no),str(target_lines[3].line_no))
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
        target_lines = find_lines(rule, proof)

        # Verify that line citations are valid
        for line in target_lines:
            result = verify_citation(current_line, line)
            if result.is_valid == False:
                return result

        # Search for lines i-j in the proof
        try:
            expressions = find_expressions(target_lines)

            # Create trees from the expressions on lines i-j
            root_i = make_tree(expressions[0])
            root_j = make_tree(expressions[1])

            # Create a tree from the expression on the current_line
            root_current = make_tree(current_line.expression)

            # Verify current line is the negation of line i
            if (root_current.value == '¬') and (root_current.right == root_i):
                
                # Verify line j is a contradiction
                if (root_j.value == '⊥') or (root_j.value.casefold() == 'false'):
                    response.is_valid = True
                    return response
                else:
                    response.err_msg = "Line {} should be '⊥' (Contradiction)"\
                        .format(str(target_lines[1].line_no))
                    return response

            else:
                response.err_msg = "Line {} is not the negation of line {}"\
                    .format(str(current_line.line_no),str(target_lines[0].line_no))
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
        target_lines = find_lines(rule, proof)

        # Verify that line citations are valid
        for line in target_lines:
            result = verify_citation(current_line, line)
            if result.is_valid == False:
                return result

        # Search for lines (m, n) in the proof
        try:
            expressions = find_expressions(target_lines)

            # Create trees from the expressions on lines (m, n)
            root_m = make_tree(expressions[0])
            root_n = make_tree(expressions[1])

            # Create a tree from the expression on the current_line
            root_current = make_tree(current_line.expression)

            # Verify m is the negation of n
            if (root_m.value == '¬') and (root_m.right == root_n):
                
                # Verify current line is a contradiction
                if (root_current.value == '⊥') or (root_current.value.casefold() == 'false'):
                    response.is_valid = True
                    return response
                else:
                    response.err_msg = "Line {} should be '⊥' (Contradiction)"\
                        .format(str(current_line.line_no))
                    return response

            else:
                response.err_msg = "Line {} is not the negation of line {}"\
                    .format(str(target_lines[0].line_no),str(target_lines[1].line_no))
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
    """
    rule = current_line.rule
    response = ProofResponse()

    # Attempt to find lines m-n
    try:
        target_lines = find_lines(rule, proof)

        # Verify that line citations are valid
        for line in target_lines:
            result = verify_citation(current_line, line)
            if result.is_valid == False:
                return result
        
        # Search for lines m-n in the proof
        try:
            expressions = find_expressions(target_lines)

            root_m = make_tree(expressions[0])
            root_n = make_tree(expressions[1])
            root_current = make_tree(current_line.expression)

            if (root_current.left == root_m) and (root_current.right == root_n):
                response.is_valid = True
                return response
            else:
                response.err_msg = "The expressions on lines {} and {} do not match the implication on line {}"\
                    .format(str(target_lines[0].line_no),str(target_lines[1].line_no),str(current_line.line_no))
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
        target_lines = find_lines(rule, proof)

        # Verify that line citations are valid
        for line in target_lines:
            result = verify_citation(current_line, line)
            if result.is_valid == False:
                return result

        # Search for lines (m, n) in the proof
        try:
            expressions = find_expressions(target_lines)
            
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
                    .format(str(target_lines[1].line_no),str(current_line.line_no),str(target_lines[0].line_no))
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
        target_lines = find_lines(rule, proof)

        # Verify that line citations are valid
        for line in target_lines:
            result = verify_citation(current_line, line)
            if result.is_valid == False:
                return result

        # Search for lines i-j in the proof
        try:
            expressions = find_expressions(target_lines)

            # Create trees from the expressions on lines i-j
            root_i = make_tree(expressions[0])
            root_j = make_tree(expressions[1])

            # Create a tree from the expression on the current_line
            root_current = make_tree(current_line.expression)

            # Verify line i is the negation of current line
            if (root_i.value == '¬') and (root_i.right == root_current):
                
                # Verify line j is a contradiction
                if (root_j.value == '⊥') or (root_j.value.casefold() == 'false'):
                    response.is_valid = True
                    return response
                else:
                    response.err_msg = "Line {} should be '⊥' (Contradiction)"\
                        .format(str(target_lines[1].line_no))
                    return response

            else:
                response.err_msg = "Line {} is not the negation of line {}"\
                    .format(str(target_lines[0].line_no),str(current_line.line_no))
                return response

        except:
            response.err_msg = "Line numbers are not specified correctly.  Indirect Proof: IP i-j"
            return response        

    except:
        response.err_msg = "Rule not formatted properly.  Indirect Proof: IP i-j"
        return response