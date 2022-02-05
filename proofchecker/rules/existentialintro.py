from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import clean_rule, get_line, is_name, is_var, verify_line_citation, make_tree
from .rule import Rule

class ExistentialIntro(Rule):

    name = "Existential Introduction"
    symbols = "∃I"

    def verify(self, current_line: ProofLineObj, proof: ProofObj, parser):
        """
        Verify proper impelmentation of the rule ∃I m
        (Existential Introduction)
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

                # Verify root operand of current line is ∃
                if (current.value[0] != '∃'):
                    response.err_msg = "The root operand of line {} should be the existential quantifier (∃)"\
                        .format(str(target_line.line_no))
                    return response
                
                # Verify line m and current line use the same predicate
                if (current.right.value[0] != root_m.value[0]):
                    response.err_msg = "Lines {} and {} should refer to the same predicate"\
                        .format(str(target_line.line_no), str(current_line.line_no))
                    return response

                # TODO: Verify that the predicates on both line have the same number of inputs
                count_m = 0
                count_curr = 0
                for ch in root_m.value:
                    if (is_var(ch) or is_name(ch)):
                        count_m += 1
                for ch in current.right.value:
                    if (is_var(ch) or is_name(ch)):
                        count_curr += 1

                if count_m != count_curr:
                    response.err_msg = "The predicates on lines {} and {} do not have the same number of inputs"\
                        .format(str(target_line.line_no), str(current_line.line_no))
                    return response

                # TODO: Verify that the inputs on current line are variables 

                response.is_valid = True
                return response

            except:
                response.err_msg = "Line numbers are not specified correctly.  Existential Introduction: ∃I m"
                return response

        except:
            response.err_msg = "Rule not formatted properly.  Existential Introduction: ∃I m"
            return response