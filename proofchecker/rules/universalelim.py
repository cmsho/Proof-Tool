from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import clean_rule, get_line, verify_line_citation, make_tree
from .rule import Rule

class UniversalElim(Rule):

    name = "Universal Elimination"
    symbols = "∀E"

    def verify(self, current_line: ProofLineObj, proof: ProofObj, parser):
        """
        Verify proper impelmentation of the rule ∀E m
        (Universal Elimination)
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
                root_m = make_tree(expression, parser)
                current = make_tree(current_line.expression, parser)

                # Verify root operand of line m is ∀
                if (root_m.value[0] != '∀'):
                    response.err_msg = "The root operand of line {} should be the universal quantifier (∀)"\
                        .format(str(target_line.line_no))
                    return response
                
                # Verify line m and current line use the same predicate
                if (root_m.right.value[0] != current.value[0]):
                    response.err_msg = "Lines {} and {} should refer to the same predicate"\
                        .format(str(target_line.line_no), str(current_line.line_no))
                    return response

                # TODO: Verify that line m and current line have same number of predicate inputs


                # TODO: Verify that substituting vars on line m yields current line


                response.is_valid = True
                return response

            except:
                response.err_msg = "Line numbers are not specified correctly.  Universal Elimination: ∀E m"
                return response

        except:
            response.err_msg = "Rule not formatted properly.  Universal Elimination: ∀E m"
            return response