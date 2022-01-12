from proofchecker.proof import ProofObj, ProofLineObj, ProofResponse, clean_rule, get_line, verify_line_citation, make_tree
from .rule import Rule

class Reiteration(Rule):

    name = "Reiteration"
    symbols = "R"

    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        """
        Verify proper impelmentation of the rule R m
        (Reiteration)
        """
        rule = clean_rule(current_line.rule)
        response = ProofResponse()

        # Attempt to find line m
        try:
            target_line = get_line(rule, proof)

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