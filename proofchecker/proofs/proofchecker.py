
from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import make_tree, is_conclusion, depth, clean_rule
from proofchecker.rules.rulechecker import RuleChecker
from proofchecker.utils import tflparser
from proofchecker.utils.tfllexer import IllegalCharacterError

def verify_proof(proof: ProofObj, parser):
    """
    Verify if a proof is valid, line by line.  
    Returns a ProofResponse, which contains an error message if invalid
    """
    response = ProofResponse()

    if len(proof.lines) == 0:
        response.err_msg = "Cannot validate a proof with no lines"
        return response

    for line in proof.lines:

        # Verify the line has a line number
        if not line.line_no:
            response.err_msg = "One or more lines is missing a line number"
            return response

        # Verify the line has an expression
        if (not line.expression) or (line.expression == ''):
            response.err_msg = "No expression on line {}"\
                .format(str(line.line_no))
            return response

        # Verify the expression is valid
        try:
            make_tree(line.expression, parser)
        except IllegalCharacterError as char_err:
            response.err_msg = "{} on line {}"\
                .format(char_err.message, str(line.line_no))
            return response 
        except:
            response.err_msg = "Syntax error on line {}"\
                .format(str(line.line_no))
            return response
        
        # Verify the rule is valid
        response = verify_rule(line, proof, parser)
        if not response.is_valid:
            return response

    last_line = proof.lines[len(proof.lines)-1]
    conclusion = is_conclusion(last_line, proof, parser)
    response.is_valid = True

    # If the last line is the desired conclusion, it is a full and complete proof
    if conclusion:
        if (last_line.rule.casefold() == 'assumption') or (last_line.rule.casefold() == 'assumpt'):
            response.err_msg = "Proof cannot be concluded with an assumption"
            return response            
        elif depth(last_line.line_no) > 1:
            response.err_msg = "Proof cannot be concluded within a subproof"
            return response
        else:
            response.is_valid = True
            return response

    # If not, the proof is incomplete
    else:
        response.is_valid = True
        response.err_msg = "All lines are valid, but the proof is incomplete"
        return response



RULES_CHOICES= {
    'tfl_basic': 'TFL - Basic Rules Only',
    'tfl_derived': 'TFL - Basic & Derived Rules',
    'fol_basic': 'FOL - Basic Rules Only',
    'fol_derived': 'FOL - Basic & Derived Rules',
}

def verify_rule(current_line: ProofLineObj, proof: ProofObj, parser):
    """
    Determines what rule is being applied, then calls the appropriate
    function to verify the rule is applied correctly
    """
    rule_str = clean_rule(current_line.rule)
    rule_str = rule_str.split()[0]
    rule_checker = RuleChecker()
    rule = rule_checker.get_rule(rule_str, proof)

    if rule == None:
        response = ProofResponse()
        response.err_msg = 'Rule "{}" on line {} not found in ruleset "{}"'\
            .format(rule_str, str(current_line.line_no), RULES_CHOICES.get(proof.rules))
        return response     
    else:
        return rule.verify(current_line, proof, parser)