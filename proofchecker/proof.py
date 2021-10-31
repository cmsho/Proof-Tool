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

    def __init__(self, line_no=None, formula=None, rule=None):
        self.line_no = line_no
        self.formula = formula
        self.rule = rule
    
    def __str__(self):
        return ('Line {}: {}, {}'.format(
            self.line_no,
            self.formula,
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
        ruleType = rule[0:2]
        match ruleType:
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
                pass
            case '→I':
                pass
            case '→E':
                return verify_implies_elim(current_line, proof)
            case 'IP':
                pass

def verify_and_intro(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule ∧I m, n
    (And Introduction)
    """
    rule = current_line.rule

    # Attempt to grab lines (m, n) 
    try:
        target_lines = rule[3:len(rule)]
        target_lines = target_lines.split()
        target_lines[0] = target_lines[0].replace(',', '')

        # Search for lines (m, n) in the proof
        try:
            formulas = []
            for num in target_lines:
                for line in proof.lines:
                    if float(num) == float(line.line_no):
                        formulas.append(line.formula)
                        break
            
            # Join the two formulas in a tree
            root_combined = Node('∧')
            root_combined.left = yacc.parser.parse(formulas[0])
            root_combined.right = yacc.parser.parse(formulas[1])

            # Create a tree from the current formula
            root_current = yacc.parser.parse(current_line.formula)

            # Compare the trees
            if root_combined == root_current:
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
    (And Elimination)
    """
    rule = current_line.rule

    # Attempt to grab line m 
    try:
        target_line = rule[3:len(rule)]
        target_line = target_line.strip()

        # Search for line m in the proof
        try:
            formula = None
            for line in proof.lines:
                if float(target_line) == float(line.line_no):
                    formula = line.formula
                    break
            
            # Create trees for the left and right side of the target formula
            root_target = yacc.parser.parse(formula)
            root_left = root_target.left
            root_right = root_target.right

            # Create a tree from the current formula
            root_current = yacc.parser.parse(current_line.formula)

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
    (Or Introduction)
    """
    rule = current_line.rule

    # Attempt to grab line m
    try:
        target_line = rule[3:len(rule)]
        target_line = target_line.strip()

        # Search for line m in the proof
        try:
            formula = None
            for line in proof.lines:
                if float(target_line) == float(line.line_no):
                    formula = line.formula
                    break

            # Create a tree for the target formula
            root_target = yacc.parser.parse(formula)

            # Create trees for left and right side of current formula
            root_current = yacc.parser.parse(current_line.formula)
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

def verify_implies_elim(current_line: ProofLine, proof: Proof):
    """
    Verify proper implementation of the rule →E m, n
    (Conditional Elimination (Modus Ponens))
    """
    rule = current_line.rule

    # Attempt to grab lines (m, n) 
    try:
        target_lines = rule[3:len(rule)]
        target_lines = target_lines.split()
        target_lines[0] = target_lines[0].replace(',', '')

        # Search for lines (m, n) in the proof
        try:
            formulas = []
            for num in target_lines:
                for line in proof.lines:
                    if float(num) == float(line.line_no):
                        formulas.append(line.formula)
                        break
            
            root_implies = yacc.parser.parse(formulas[0])

            root_combined = Node('→')
            root_combined.left = yacc.parser.parse(formulas[1])
            root_combined.right = yacc.parser.parse(current_line.formula)

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