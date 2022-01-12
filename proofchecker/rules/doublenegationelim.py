from proofchecker.proof import ProofObj, ProofLineObj, ProofResponse, clean_rule, get_line_DNE, verify_line_citation, make_tree
from .rule import Rule

class DoubleNegationElim(Rule):

    name = "Double Negation Elimination"
    symbols = "DNE"

    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        """
        Verify the proper implementation of DNE m
        (Double Not Elimination)
        """
        rule = clean_rule(current_line.rule)
        response = ProofResponse()

        # Attempt to find line m
        try:
            target_line = get_line_DNE(rule, proof)

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