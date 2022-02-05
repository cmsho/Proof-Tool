from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import clean_rule, get_line, verify_line_citation, make_tree, is_name, is_var
from .rule import Rule

class UniversalIntro(Rule):

    name = "Universal Introduction"
    symbols = "∀I"

    def verify(self, current_line: ProofLineObj, proof: ProofObj, parser):
        """
        Verify proper impelmentation of the rule ∀I m
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
                root_m = make_tree(target_line.expression, parser)
                current = make_tree(current_line.expression, parser)

                # Verify root operand of current line is ∀
                if (current.value[0] != '∀'):
                    response.err_msg = "The root operand of line {} should be the universal quantifier (∀)"\
                        .format(str(target_line.line_no))
                    return response
                
                # Verify line m and current line use the same predicate
                if (current.right.value[0] != root_m.value[0]):
                    response.err_msg = "Lines {} and {} should refer to the same predicate"\
                        .format(str(target_line.line_no), str(current_line.line_no))
                    return response

                # Verify that the predicates on both line have the same number of inputs
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

                # Verify that each variable instance on current line represents the same name on line m
                var = current.value[1]
                index = 0
                var_indexes = []

                # Eliminate whitespace in the functions to avoid issues
                func_m = root_m.value.replace(' ', '')
                func_curr = current.right.value.replace(' ', '')

                # Make sure the bound variable does not appear in line m
                for ch in func_m:
                    if ch == var:
                        response.err_msg = "Variable {} on line {} should not appear on line {}"\
                            .format(var, str(current_line.line_no), str(target_line.line_no))
                        return response                        

                # Keep track of the locations (indexes) of the bound variable on current line
                for ch in func_curr:
                    if ch == var:
                        var_indexes.append(index)
                    index += 1

                # Get the values at these locations in line m
                # Make sure they all represent names
                names = []
                for i in var_indexes:
                    names.append(func_m[i])
                
                for ch in names:
                    if not is_name(ch):
                        response.err_msg = "Instances of variable {} on line {} should be represent a name on line {}"\
                            .format(var, str(current_line.line_no), str(target_line.line_no))
                        return response
                
                # Make sure they all use the same name
                if len(names) > 1:
                    for ch in names:
                        if not ch == names[0]:
                            response.err_msg = "All instances of variable {} on line {} should be represent the same name on line {}"\
                                .format(var, str(current_line.line_no), str(target_line.line_no))
                            return response


                # Now, check that all instances of this name in line_m are replaced by the same (bound) var in current line
                name = names[0]
                index = 0
                name_indexes = []

                # Keep track of the locations (indexes) of the bound variable on current line
                for ch in func_m:
                    if ch == name:
                        name_indexes.append(index)
                    index += 1

                # Get the values at these locations in the current line
                # Make sure they all are replaced by the bound variable
                vars = []
                for i in name_indexes:
                    vars.append(func_curr[i])

                for ch in vars:
                    if not (ch == var):
                        response.err_msg = "All instances of name {} on line {} should be replaced with the bound variable {} on line {}"\
                            .format(name, str(target_line.line_no), var, str(current_line.line_no))
                        return response

                response.is_valid = True
                return response

            except:
                response.err_msg = "Line numbers are not specified correctly.  Universal Introduction: ∀I m"
                return response

        except:
            response.err_msg = "Rule not formatted properly.  Universal Introduction: ∀I m"
            return response
