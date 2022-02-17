from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import clean_rule, get_line, verify_line_citation, make_tree, is_name, is_var
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
            result = verify_line_citation(current_line.line_no, target_line.line_no)
            if result.is_valid == False:
                return result

            try: 
                root_m = make_tree(target_line.expression, parser)
                current = make_tree(current_line.expression, parser)

                # Verify root operand of line m is ∀
                if (root_m.value[0] != '∀'):
                    response.err_msg = "Error on line {}: The root operand of line {} should be the universal quantifier (∀)"\
                        .format(str(current_line.line_no), str(target_line.line_no))
                    return response
                
                # Verify line m and current line use the same predicate
                if (root_m.right.value[0] != current.value[0]):
                    response.err_msg = "Error on line {}: Lines {} and {} should refer to the same predicate"\
                        .format(str(current_line.line_no), str(target_line.line_no), str(current_line.line_no))
                    return response

                # Verify that line m and current line have same number of predicate inputs
                count_m = 0
                count_curr = 0
                for ch in root_m.right.value:
                    if (is_var(ch) or is_name(ch)):
                        count_m += 1
                for ch in current.value:
                    if (is_var(ch) or is_name(ch)):
                        count_curr += 1

                if count_m != count_curr:
                    response.err_msg = "Error on line {}: The predicates on lines {} and {} do not have the same number of inputs"\
                        .format(str(current_line.line_no), str(target_line.line_no), str(current_line.line_no))
                    return response

                # Verify that each variable reference on line m is replaced by the same name on current line
                var = root_m.value[1]
                index = 0
                var_indexes = []

                # Eliminate whitespace in the functions to avoid issues
                func_m = root_m.right.value.replace(' ', '')
                func_curr = current.value.replace(' ', '')

                # Keep track of the locations (indexes) of the bound variable on line m
                for ch in func_m:
                    if ch == var:
                        var_indexes.append(index)
                    index += 1

                # Get the values at these locations in the current line
                # Make sure they all represent names
                names = []
                for i in var_indexes:
                    names.append(func_curr[i])
                
                for ch in names:
                    if not is_name(ch):
                        response.err_msg = "Error on line {}: Instances of variable {} on line {} should be replaced with a name on line {}"\
                            .format(str(current_line.line_no), var, str(target_line.line_no), str(current_line.line_no))
                        return response
                
                # Make sure they all use the same name
                if len(names) > 1:
                    for ch in names:
                        if not ch == names[0]:
                            response.err_msg = "Error on line {}: All instances of variable {} on line {} should be replaced with the same name on line {}"\
                                .format(str(current_line.line_no), var, str(target_line.line_no), str(current_line.line_no))
                            return response

                response.is_valid = True
                return response

            except:
                response.err_msg = "Error on line {}: Line numbers are not specified correctly.  Universal Elimination: ∀E m"\
                    .format(str(current_line.line_no))
                return response

        except:
            response.err_msg = "Error on line {}: Rule not formatted properly.  Universal Elimination: ∀E m"\
                .format(str(current_line.line_no))
            return response