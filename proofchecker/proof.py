from proofchecker.models import ProofLine
from proofchecker.utils.tfllex import IllegalCharacterError
from .utils import tflparse, numparse
from .utils.tfllex import lexer as tfllexer
from .utils.numlex import lexer as numlexer
from .utils.binarytree import Node

class ProofObj:
    
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

class ProofLineObj:

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

def is_valid_expression(expression: str):
    """
    Verify if a string is a valid Boolean expression
    Returns a Boolean (True/False)
    """
    # Verify the expression is valid
    try:
        expression = make_tree(expression)
        if expression == None:
            return False
        else:
            return True
    except:
        return False

def verify_expression(expression: str):
    """
    Verify if a string is a valid boolean expression
    Returns a ProofResponse
    """
    response = ProofResponse()
    # Verify the expression is valid
    try:
        expression = make_tree(expression)
        if expression == None:
            response.err_msg = "Expression cannot be an empty string"
            return response
        else:
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

def verify_proof(proof: ProofObj):
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
    if rule[0] in '~-':
        clean_rule = '¬' + rule[1:len(rule)]
        return clean_rule
    if (rule[0] == '>') or (rule[0:2] == '->'):
        clean_rule = '→' + rule[1:len(rule)]
        return clean_rule
    return rule

def verify_rule(current_line: ProofLineObj, proof: ProofObj):
    """
    Determines what rule is being applied, then calls the appropriate
    function to verify the rule is applied correctly
    """
    rule = clean_rule(current_line.rule)

    if rule.casefold() == 'premise':
        return verify_premise(current_line, proof)
    elif (rule.casefold() == 'assumption') or (rule.casefold() == 'assumpt'):
        return verify_assumption(current_line)
    elif rule[0].casefold() == 'x':
        return verify_explosion(current_line, proof)
    elif rule[0].casefold() == 'r':
        return verify_reiteration(current_line, proof)
    elif rule[0:3].casefold() == 'dne':
        return verify_double_not_elim(current_line, proof)
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
            case '↔I':
                return verify_iff_intro(current_line, proof)
            case '↔E':
                return verify_iff_elim(current_line, proof)

    
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
        response.err_msg = "Line numbers are not formatted properly"
        return response

def verify_subproof_citation(current_line: ProofLineObj, cited_line: ProofLineObj):
    """
    Verify whether an subproof citation is valid
    Returns a ProofResponse with an error message if invalid
    """
    # Currently subproof cited as lines i-j
    #       i = first line of subproof (e.g. 2.1)
    #       j = last line of subproof  (e.g. 2.4)
    #
    # TODO: Refactor code so citation
    #       only requires one line     (e.g. 2)

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


def make_tree(string: str):
    """
    Function to construct a binary tree
    """
    return tflparse.parser.parse(string, lexer=tfllexer)

def is_conclusion(current_line: ProofLineObj, proof: ProofObj):
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


def find_premises(premises: str):
    """
    Take a string of comma separated-premises
    and return an array of premises
    """
    premises = premises.replace(',', ' ')
    premises = premises.split()
    return premises

def find_line(rule: str, proof: ProofObj):
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

def find_line_x_r(rule: str, proof: ProofObj):
    """
    Find a single line from the TFL rules X and R
    """
    target_line_no = rule[2:len(rule)]
    target_line_no = target_line_no.strip()
    target_line = None
    for line in proof.lines:
        if str(target_line_no) == str(line.line_no):
            target_line = line
            break
    return target_line

def find_lines(rule: str, proof: ProofObj):
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

def verify_premise(current_line: ProofLineObj, proof: ProofObj):
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

def verify_assumption(current_line: ProofLineObj):
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

def verify_reiteration(current_line: ProofLineObj, proof: ProofObj):
    """
    Verify proper impelmentation of the rule R m
    (Reiteration)
    """
    rule = clean_rule(current_line.rule)
    response = ProofResponse()

    # Attempt to find line m
    try:
        target_line = find_line_x_r(rule, proof)

        # Verify if line citation is valid
        result = verify_line_citation(current_line, target_line)
        if result.is_valid == False:
            return result

        try: 
            expression = target_line.expression
            root_m = make_tree(expression)
            current = make_tree(current_line.expression)

            # Verify line m and current line are equivalent
            if (root_m == current):
                response.is_valid = True
                return response
            else:
                response.err_msg = "Lines {} and {} are not equivalent"\
                    .format(str(target_line.line_no), str(current_line.line_no))
                return response

        except:
            response.err_msg = "Line numbers are not specified correctly.  Reiteration: R m"
            return response      

    except:
        response.err_msg = "Rule not formatted properly.  Reiteration: R m"
        return response 

def verify_explosion(current_line: ProofLineObj, proof: ProofObj):
    """
    Verify proper implementation of the rule X m
    (Explosion)
    """
    rule = clean_rule(current_line.rule)
    response = ProofResponse()

    # Attempt to find line m
    try:
        target_line = find_line_x_r(rule, proof)

        # Verify if line citation is valid
        result = verify_line_citation(current_line, target_line)
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
        response.err_msg = "Rule not formatted properly.  Explosion: X m"
        return response 

def verify_and_intro(current_line: ProofLineObj, proof: ProofObj):
    """
    Verify proper implementation of the rule ∧I m, n
    (Conjunction Introduction)
    """
    rule = clean_rule(current_line.rule)
    response = ProofResponse()

    # Attempt to find lines (m, n) 
    try:
        target_lines = find_lines(rule, proof)

        for line in target_lines:
            result = verify_line_citation(current_line, line)
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
            if (root_current == root_m_and_n) or (root_current == root_n_and_m):
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

def verify_and_elim(current_line: ProofLineObj, proof: ProofObj):
    """
    Verify proper implementation of the rule ∧E m
    (Conjunction Elimination)
    """
    rule = clean_rule(current_line.rule)
    response = ProofResponse()

    # Attempt to find line m 
    try:
        target_line = find_line(rule, proof)

        # Verify if line citation is valid
        result = verify_line_citation(current_line, target_line)
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
            if (root_current == root_left) or (root_current == root_right):
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

def verify_or_intro(current_line: ProofLineObj, proof: ProofObj):
    """
    Verify proper implementation of the rule ∨I m
    (Disjunction Introduction)
    """
    rule = clean_rule(current_line.rule)
    response = ProofResponse()

    # Attempt to find line m
    try:
        target_line = find_line(rule, proof)

        # Verify if line citation is valid
        result = verify_line_citation(current_line, target_line)
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
            if (root_target == root_left) or (root_target == root_right):
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


def verify_or_elim(current_line: ProofLineObj, proof: ProofObj):
    """
    Verify proper implementation of the rule ∨E m, i-j, k-l
    (Disjunction Elimination)
    """
    rule = clean_rule(current_line.rule)
    response = ProofResponse()

    # Attempt to find lines (m, i-j, k-l)
    try:
        target_lines = find_lines(rule, proof)

        # Verify that line m citation is valid
        line_m_citation = verify_line_citation(current_line, target_lines[0])
        if line_m_citation.is_valid == False:
            return line_m_citation

        # Verify that subproof citations are valid
        for line in target_lines[1:len(target_lines)]:
            result = verify_subproof_citation(current_line, line)
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


def verify_not_intro(current_line: ProofLineObj, proof: ProofObj):
    """
    Verify proper implementation of the rule ¬I m-n
    (Negation Introduction)
    """
    rule = clean_rule(current_line.rule)
    response = ProofResponse()

    # Attempt to find lines (i-j)
    try:
        target_lines = find_lines(rule, proof)

        # Verify that subproof citation are valid
        for line in target_lines:
            result = verify_subproof_citation(current_line, line)
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


def verify_not_elim(current_line: ProofLineObj, proof: ProofObj):
    """
    Verify proper implementation of the rule ¬E m, n
    (Negation Elimination)
    """
    rule = clean_rule(current_line.rule)
    response = ProofResponse()

    # Attempt to find lines (m, n)
    try:
        target_lines = find_lines(rule, proof)

        # Verify that line citations are valid
        for line in target_lines:
            result = verify_line_citation(current_line, line)
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


def verify_implies_intro(current_line: ProofLineObj, proof: ProofObj):
    """
    Verify proper implementation of the rule →I m-n
    (Conditional Introduction)
    """
    rule = clean_rule(current_line.rule)
    response = ProofResponse()

    # Attempt to find lines m-n
    try:
        target_lines = find_lines(rule, proof)

        # Verify that subproof citation are valid
        for line in target_lines:
            result = verify_subproof_citation(current_line, line)
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


def verify_implies_elim(current_line: ProofLineObj, proof: ProofObj):
    """
    Verify proper implementation of the rule →E m, n
    (Conditional Elimination (Modus Ponens))
    """
    rule = clean_rule(current_line.rule)
    response = ProofResponse()

    # Attempt to find lines (m, n) 
    try:
        target_lines = find_lines(rule, proof)

        # Verify that line citations are valid
        for line in target_lines:
            result = verify_line_citation(current_line, line)
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


def verify_indirect_proof(current_line: ProofLineObj, proof: ProofObj):
    """
    Verify proper implementation of the rule IP i-j
    (Indirect Proof)
    """
    rule = clean_rule(current_line.rule)
    response = ProofResponse()

    # Attempt to find lines i-j
    try:
        target_lines = find_lines(rule, proof)

        # Verify that subproof citation are valid
        for line in target_lines:
            result = verify_subproof_citation(current_line, line)
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

def verify_iff_intro(current_line: ProofLineObj, proof: ProofObj):
    """
    Verify the rule ↔I i-j, k-l
    (Biconditional Introduction)
    """
    rule = clean_rule(current_line.rule)
    response = ProofResponse()

    # Attempt to find lines (i-j, k-l)
    try:
        target_lines = find_lines(rule, proof)

        # Verify that subproof citations are valid
        for line in target_lines:
            result = verify_subproof_citation(current_line, line)
            if result.is_valid == False:
                return result

        # Search for lines i-j, k-l in the proof
        try:
            expressions = find_expressions(target_lines)

            # Create trees for expressions on lines i, j, k, and l
            root_i = make_tree(expressions[0])
            root_j = make_tree(expressions[1])
            root_k = make_tree(expressions[2])
            root_l = make_tree(expressions[3])
            root_current = make_tree(current_line.expression)

            # Verify lines i and l are equivalent
            if root_i == root_l:
                # Verify that lines j and k are equivalent
                if root_j == root_k:
                    # If i and j are equivalent, left and right of current should also be equivalent
                    if root_i==root_j:
                        if (root_current.left == root_i) and (root_current.left == root_current.right):
                            response.is_valid = True
                            return response
                        else:
                            response.err_msg = "Invalid introduction on line {}"\
                                .format(str(current_line.line_no))
                            return response

                    else:
                        # If i and j are not equivalent, left side of current line should equal i or j,
                        # and right side of current line should equal i or j,
                        # and left side should not equal right side
                        if (root_current.left == root_i) or (root_current.left == root_j):
                            if (root_current.right == root_i) or (root_current.right == root_j):
                                if root_current.left != root_current.right:
                                    response.is_valid = True
                                    return response
                                else:
                                    response.err_msg = "Left side and right side of line {} are equiavlent, but lines {} and {} are not equivalent"\
                                        .format(str(current_line.line_no), str(target_lines[0].line_no), str(target_lines[1].line_no))
                                    return response
                            else:
                                    response.err_msg = "Right side of line {} does not equal either of the expressions on lines {} and {}"\
                                        .format(str(current_line.line_no), str(target_lines[1].line_no), str(target_lines[3].line_no))
                                    return response
                        else:
                                response.err_msg = "Left side of line {} does not equal either of the expressions on lines {} and {}"\
                                    .format(str(current_line.line_no), str(target_lines[1].line_no), str(target_lines[3].line_no))
                                return response
                else:
                    response.err_msg = "The expressions on lines {} and {} are not equivalent"\
                        .format(str(target_lines[1].line_no),str(target_lines[2].line_no))
                    return response
            else:
                response.err_msg = "The expressions on lines {} and {} are not equivalent"\
                    .format(str(target_lines[0].line_no),str(target_lines[3].line_no))
                return response
        except:
            response.err_msg = "Line numbers are not specified correctly.  ↔I i-j, k-l"
            return response        
    except:
        response.err_msg = "Rule not formatted properly.  ↔I i-j, k-l"
        return response

def verify_iff_elim(current_line: ProofLine, proof: ProofObj):
    """
    Verify the rule ↔E m, n
    (Biconditional Elimination)
    """
    rule = clean_rule(current_line.rule)
    response = ProofResponse()

    # Attempt to find lines (m, n) 
    try:
        target_lines = find_lines(rule, proof)

        for line in target_lines:
            result = verify_line_citation(current_line, line)
            if result.is_valid == False:
                return result

        # Search for lines (m, n) in the proof
        try:
            expressions = find_expressions(target_lines)
            
            # Join the two expressions in a tree
            root_m = make_tree(expressions[0])
            root_n = make_tree(expressions[1])
            root_current = make_tree(current_line.expression)

            # Compare the trees
            if (root_n == root_m.left) or (root_n == root_m.right):
                if (root_current == root_m.left) or (root_current == root_m.right):
                    if (root_m.left == root_m.right) or (root_n != root_current):
                        response.is_valid = True
                        return response
                    else:
                        response.err_msg = "The expressions on lines {} and {} do not represent both the left and right side of the expression on line {}"\
                            .format(str(target_lines[1].line_no), str(current_line.line_no), str(target_lines[0].line_no))
                        return response
                else:
                    response.err_msg = "The expression on line {} does not represent the left or right side of the expression on line {}"\
                        .format(str(current_line.line_no), str(target_lines[0].line_no))
                    return response
            else:
                response.err_msg = "The expression on line {} does not represent the left or right side of the expression on line {}"\
                    .format(str(target_lines[1].line_no), str(target_lines[0].line_no))
                return response
        
        except:
            response.err_msg = "Line numbers are not specified correctly.  Biconditional Elimination: ↔E m, n"
            return response

    except:
        response.err_msg = "Rule is not formatted properly.  Biconditional Elimination: ↔E m, n"
        return response

def verify_double_not_elim(current_line: ProofLineObj, proof: ProofObj):
    """
    Verify the proper implementation of DNE m
    (Double Not Elimination)
    """
    rule = clean_rule(current_line.rule)
    response = ProofResponse()

    # Attempt to find line m
    try:
        target_line = find_line(rule, proof)

        # Verify if line citation is valid
        result = verify_line_citation(current_line, target_line)
        if result.is_valid == False:
            return result

        # Search for line m in the proof
        try:
            expression = target_line.expression

            # Create trees
            root_m = make_tree(expression)
            root_current = make_tree(current_line.expression)


            if root_m.value == '¬':
                if root_m.right.value == '¬':
                    if root_m.right.right == root_current:
                        response.is_valid = True
                        return response
                    else:
                        response.err_msg = "Lines {} and {} are not equivalent"\
                            .format(str(target_line.line_no), str(current_line.line_no))
                        return response
                else:
                    response.err_msg = "Line {} is not an instance of double-not operators"\
                        .format(str(target_line.line_no))
                    return response
            else:
                response.err_msg = "The main logical operator on line {} is not '¬'"\
                    .format(str(target_line.line_no))
                return response

        except:
            response.err_msg = "Line numbers are not specified correctly.  Double Not Elimination: DNE m"
            return response

    except:
        response.err_msg = "Rule not formatted properly.  Double Not Elimination: DNE m"
        return response