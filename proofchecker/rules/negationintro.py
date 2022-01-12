from proofchecker.proof import ProofObj, ProofLineObj, ProofResponse, clean_rule, make_tree, get_line_no, get_lines_in_subproof, verify_subproof_citation, get_expressions
from .rule import Rule

class NegationIntro(Rule):

    name = "Negation Introduction"
    symbols = "¬I"

    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        """
        Verify proper implementation of the rule ¬I m
        (Negation Introduction)
        """
        rule = clean_rule(current_line.rule)
        response = ProofResponse()

        # Attempt to find lines (i-j)
        try:
            target_line_no = get_line_no(rule)
            target_lines = get_lines_in_subproof(target_line_no, proof)

            # Verify that subproof citation are valid
            for line in target_lines:
                result = verify_subproof_citation(current_line, line)
                if result.is_valid == False:
                    return result

            # Search for lines i-j in the proof
            try:
                expressions = get_expressions(target_lines)

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
                response.err_msg = "Line numbers are not specified correctly.  Negation Introduction: ¬I m"
                return response        

        except:
            response.err_msg = "Rule not formatted properly.  Negation Introduction: ¬I m"
            return response