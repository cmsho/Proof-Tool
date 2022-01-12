from proofchecker.proof import ProofObj, ProofLineObj, ProofResponse, clean_rule, get_line_no, verify_subproof_citation, make_tree, get_expressions, get_lines_in_subproof
from .rule import Rule

class IndirectProof(Rule):

    name = "Indirect Proof"
    symbols = "IP"

    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        """
        Verify proper implementation of the rule IP m
        (Indirect Proof)
        """
        rule = clean_rule(current_line.rule)
        response = ProofResponse()

        # Attempt to find lines m
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
                response.err_msg = "Line numbers are not specified correctly.  Indirect Proof: IP m"
                return response        

        except:
            response.err_msg = "Rule not formatted properly.  Indirect Proof: IP m"
            return response