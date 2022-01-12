from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import Node, clean_rule, get_lines, verify_line_citation, make_tree, get_expressions
from .rule import Rule

class ConditionalElim(Rule):

    name = "Conditional Elimination"
    symbols = "→E"

    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        """
        Verify proper implementation of the rule →E m, n
        (Conditional Elimination (Modus Ponens))
        """
        rule = clean_rule(current_line.rule)
        response = ProofResponse()

        # Attempt to find lines (m, n) 
        try:
            target_lines = get_lines(rule, proof)

            # Verify that line citations are valid
            for line in target_lines:
                result = verify_line_citation(current_line, line)
                if result.is_valid == False:
                    return result

            # Search for lines (m, n) in the proof
            try:
                expressions = get_expressions(target_lines)
                
                root_implies = make_tree(expressions[0])

                root_combined = Node('→')
                root_combined.left = make_tree(expressions[1])
                root_combined.right = make_tree(current_line.expression)

                # Compare the trees
                if root_implies == root_combined:
                    response.is_valid = True
                    return response
                else:
                    response.err_msg = "The expressions on lines {} and {} do not match the implication on line {}"\
                        .format(str(target_lines[1].line_no),str(current_line.line_no),str(target_lines[0].line_no))
                    return response
            
            except:
                response.err_msg = "Line numbers are not specified correctly.  Conditional Elimination (Modus Ponens): →E m, n"
                return response

        except:
            response.err_msg = "Rule not formatted properly.  Conditional Elimination (Modus Ponens): →E m, n"
            return response