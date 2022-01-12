from proofchecker.proof import ProofObj, ProofLineObj, ProofResponse, clean_rule, get_line, verify_line_citation, make_tree
from .rule import Rule

class DisjunctionIntro(Rule):

    name = "Disjunction Introduction"
    symbols = "∨I"

    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        """
        Verify proper implementation of the rule ∨I m
        (Disjunction Introduction)
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