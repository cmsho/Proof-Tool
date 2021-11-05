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

def verify_rule(current_line: ProofLine, proof: Proof):
    """
    Determines what rule is being applied, then calls the appropriate
    function to verify the rule is applied correctly
    """
    rule = current_line.rule

    if rule.casefold() == 'premise':
        pass
    elif rule.casefold() == ('assumption' or 'assumpt'):
        pass
    elif rule.casefold() == 'x':
        pass
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
                pass
            case '¬I':
                pass
            case '¬E':
                return verify_not_elim(current_line, proof)
            case '→I':
                pass
            case '→E':
                return verify_implies_elim(current_line, proof)
            case 'IP':
                pass

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

    # Attempt to find lines (m, n) 
    try:
        target_lines = find_lines(rule)

        # Search for lines (m, n) in the proof
        try:
            expressions = find_expressions(target_lines, proof)
            
            # Join the two expressions in a tree
            root_combined = Node('∧')
            root_combined.left = make_tree(expressions[0])
            root_combined.right = make_tree(expressions[1])

            root_combined_reverse = Node('∧')
            root_combined_reverse.left = make_tree(expressions[1])
            root_combined_reverse.right = make_tree(expressions[0])

            # Create a tree from the current expression
            root_current = make_tree(current_line.expression)

            # Compare the trees
            if root_current == (root_combined or root_combined_reverse):
                return True
            else:
                return False
        
        except:
            print("Line numbers are not specified correctly")
            return False

    except:
        print("Rule not formatted properly")
        return False

def verify_and_elim(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule ∧E m
    (Conjunction Elimination)
    """
    rule = current_line.rule

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
                return True
            else:
                return False
        
        except:
            print("Line numbers are not specified correctly")
            return False      

    except:
        print("Rule not formatted properly")
        return False

def verify_or_intro(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule ∨I m
    (Disjunction Introduction)
    """
    rule = current_line.rule

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
                return True
            else:
                return False

        except:
            print("Line numbers are not specified correctly")
            return False        

    except:
        print("Rule not formatted properly")
        return False


def verify_or_elim(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule ∨E m, i-j, k-l
    (Disjunction Elimination)
    """
    rule = current_line.rule

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
                            return True
                        else:
                            response = "The expressions on lines {}, {} and {} are not equivalent"\
                                .format(str(target_lines[2]),str(target_lines[4]),str(current_line.line_no))
                            print(response)
                            return False
                    else:
                        response = "The expressions on line {} is not part of the disjunction on line {}"\
                            .format(str(target_lines[3]),str(target_lines[0]))
                        print(response)
                        return False
                else:
                    response = "The expressions on line {} is not part of the disjunction on line {}"\
                        .format(str(target_lines[1]),str(target_lines[0]))
                    print(response)
                    return False                                                    
            else:
                response = "The expressions on lines {} and {} should be different"\
                    .format(str(target_lines[1]),str(target_lines[3]))
                print(response)
                return False    
        except:
            print("Line numbers are not specified correctly")
            return False        
    except:
        print("Rule not formatted properly")
        return False

def verify_not_elim(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule ¬E m, n
    (Negation Elimination)
    """
    rule = current_line.rule

    # Attempt to find lines (m, n)
    try:
        target_lines = find_lines(rule)

        # Search for line m in the proof
        try:
            expressions = find_expressions(target_lines, proof)

            # Create trees from the expression on line (m, n)
            root_m = make_tree(expressions[0])
            root_n = make_tree(expressions[1])

            # Create a tree from the expression on the current_line
            root_current = make_tree(current_line.expression)

            # Verify m is the negation of n
            if (root_m.value == '¬') and (root_m.right == root_n):
                
                # TODO: Test this
                if (root_current.value == '⊥') or (root_current.value.casefold() == 'false'):
                    return True
                else:
                    response = "Line {} should be '⊥' (Contradiction)"\
                        .format(str(current_line.line_no))
                    return False

            else:
                response = "Line {} is not the negation of line {}"\
                    .format(str(target_lines[0]),str(target_lines[1]))
                print(response)
                return False

        except:
            print("Line numbers are not specified correctly")
            return False        

    except:
        print("Rule not formatted properly")
        return False


def verify_implies_intro(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule →I m-n
    (Conditional Introduction)
    TODO: Verify that it is legal to reference the line numbers
    """
    rule = current_line.rule

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
                return True
            else:
                response = "The expressions on lines {} and {} do not match the implication on line {}"\
                    .format(str(target_lines[0]),str(target_lines[1]),str(current_line.line_no))
                print(response)
                return False

        except:
            print("Line numbers are not specified correctly")
            return False

    except:
        print("Rule not formatted properly")
        return False    
def verify_implies_elim(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule →E m, n
    (Conditional Elimination (Modus Ponens))
    """
    rule = current_line.rule

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
                return True
            else:
                return False
        
        except:
            print("Line numbers are not specified correctly")
            return False

    except:
        print("Rule not formatted properly")
        return False    