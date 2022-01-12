from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import clean_rule, get_line_nos, get_lines_in_subproof, verify_subproof_citation, make_tree, get_expressions
from .rule import Rule

class BiconditionalIntro(Rule):

    name = "Biconditional Introduction"
    symbols = "↔I"

    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        """
        Verify the rule ↔I i, j
        (Biconditional Introduction)
        """
        rule = clean_rule(current_line.rule)
        response = ProofResponse()

        # Attempt to find lines in subproofs i and j
        try:
            target_line_nos = get_line_nos(rule)
            lines_i = get_lines_in_subproof(target_line_nos[0], proof)
            lines_j = get_lines_in_subproof(target_line_nos[1], proof)
            target_lines = [lines_i[0], lines_i[1], lines_j[0], lines_j[1]]

            # Verify that subproof citations are valid
            for line in target_lines:
                result = verify_subproof_citation(current_line, line)
                if result.is_valid == False:
                    return result

            # Search for lines i-j, k-l in the proof
            try:
                expressions = get_expressions(target_lines)

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
                response.err_msg = "Line numbers are not specified correctly.  ↔I i, j"
                return response        
        except:
            response.err_msg = "Rule not formatted properly.  ↔I i, j"
            return response