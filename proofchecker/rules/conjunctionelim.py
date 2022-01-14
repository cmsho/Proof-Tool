from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import Node, clean_rule, get_line, make_tree, verify_line_citation
from .rule import Rule

class ConjunctionElim(Rule):

    name = 'Conjunction Elimination'
    symbols = '∧E'

    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        """
        Verify proper implementation of the rule ∧E m
        (Conjunction Elimination)
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
                
                # Create trees for the left and right side of the target expression
                root_target = make_tree(expression)
                root_left = root_target.left
                root_right = root_target.right

                # Create a tree from the current expression
                root_current = make_tree(current_line.expression)

                # Compare the trees
                if (root_current == root_left) or (root_current == root_right):
                    response.is_valid = True
                    return response
                else:
                    response.err_msg = "Line {} does not follow from line {}"\
                        .format(str(current_line.line_no), str(target_line.line_no))
                    return response
            
            except:
                response.err_msg = "Line numbers are not specified correctly.  Conjunction Elimination: ∧E m"
                return response      

        except:
            response.err_msg = "Rule not formatted properly.  Conjunction Elimination: ∧E m"
            return response