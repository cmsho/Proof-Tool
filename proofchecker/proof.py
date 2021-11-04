from .utils import tflparse as yacc
from .utils.binarytree import Node, treeToString

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

def grab_one_line(rule: str):
    """
    Grab line (m) from a TFL rule
    """
    target_line = rule[3:len(rule)]
    target_line = target_line.strip()
    return target_line

def grab_two_lines(rule: str):
    """
    Grab lines (m, n) from a TFL rule
    """
    target_lines = rule[3:len(rule)]
    target_lines = target_lines.split()
    target_lines[0] = target_lines[0].replace(',', '')
    return target_lines

def grab_line_group(rule: str):
    """
    Grab lines m-n from a TFL rule
    """
    target_lines = rule[3:len(rule)]
    target_lines = target_lines.replace('-', ' ')
    target_lines = target_lines.split()
    return target_lines

def grab_two_line_groups(rule: str):
    """
    Grab lines i-j, k-l from a TFL rule
    """
    target_lines = rule[3:len(rule)]
    target_lines = target_lines.replace('-', ' ')
    target_lines = target_lines.replace(',', '')
    target_lines = target_lines.split()
    return target_lines

def find_one_expression(target_line: int, proof: Proof):
    """
    Find the expression on line (m) of a Proof
    """
    expression = None
    for line in proof.lines:
        if float(target_line) == float(line.line_no):
            expression = line.expression
            break
    return expression

def find_two_expressions(target_lines: list[int], proof: Proof):
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

    # Attempt to grab lines (m, n) 
    try:
        target_lines = grab_two_lines(rule)

        # Search for lines (m, n) in the proof
        try:
            expressions = find_two_expressions(target_lines, proof)
            
            # Join the two expressions in a tree
            root_combined = Node('∧')
            root_combined.left = yacc.parser.parse(expressions[0])
            root_combined.right = yacc.parser.parse(expressions[1])

            root_combined_reverse = Node('∧')
            root_combined_reverse.left = yacc.parser.parse(expressions[1])
            root_combined_reverse.right = yacc.parser.parse(expressions[0])

            # Create a tree from the current expression
            root_current = yacc.parser.parse(current_line.expression)

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

    # Attempt to grab line m 
    try:
        target_line = grab_one_line(rule)

        # Search for line m in the proof
        try:
            expression = find_one_expression(target_line, proof)
            
            # Create trees for the left and right side of the target expression
            root_target = yacc.parser.parse(expression)
            root_left = root_target.left
            root_right = root_target.right

            # Create a tree from the current expression
            root_current = yacc.parser.parse(current_line.expression)

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

    # Attempt to grab line m
    try:
        target_line = grab_one_line(rule)

        # Search for line m in the proof
        try:
            expression = find_one_expression(target_line, proof)

            # Create a tree for the target expression
            root_target = yacc.parser.parse(expression)

            # Create trees for left and right side of current expression
            root_current = yacc.parser.parse(current_line.expression)
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


def verify_not_elim(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule ¬E m, n
    (Negation Elimination)
    """
    rule = current_line.rule

    # Attempt to grab lines (m, n)
    try:
        target_lines = grab_two_lines(rule)

        # Search for line m in the proof
        try:
            expressions = find_two_expressions(target_lines, proof)

            # Create trees from the expression on line (m, n)
            root_m = yacc.parser.parse(expressions[0])
            root_n = yacc.parser.parse(expressions[1])

            # Create a tree from the expression on the current_line
            root_current = yacc.parser.parse(current_line.expression)

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

    # Attempt to grab lines m-n
    try:
        target_lines = grab_line_group(rule)
        
        # Search for lines m-n in the proof
        try:
            expressions = find_two_expressions(target_lines, proof)

            root_m = yacc.parser.parse(expressions[0])
            root_n = yacc.parser.parse(expressions[1])
            root_current = yacc.parser.parse(current_line.expression)

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

    # Attempt to grab lines (m, n) 
    try:
        target_lines = grab_two_lines(rule)

        # Search for lines (m, n) in the proof
        try:
            expressions = find_two_expressions(target_lines, proof)
            
            root_implies = yacc.parser.parse(expressions[0])

            root_combined = Node('→')
            root_combined.left = yacc.parser.parse(expressions[1])
            root_combined.right = yacc.parser.parse(current_line.expression)

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