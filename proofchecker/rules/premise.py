from proofchecker.proof import ProofObj, ProofLineObj, ProofResponse, make_tree
from .rule import Rule

class Premise(Rule):

    name = "Premise"
    symbols = "Premise"

    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        """
        Verify that "premise" is valid justification for a line
        """
        response = ProofResponse()
        try:
            current_exp = current_line.expression
            current = make_tree(current_exp)

            # If there is only one premise
            if isinstance(proof.premises, str):
                if make_tree(proof.premises) == current:
                    response.is_valid = True
                    return response
                else:
                    response.err_msg = "Expression on line {} is not a premise"\
                        .format(str(current_line.line_no))
                    return response                

            # If multiple expressions, search for the premise
            for premise in proof.premises:
                if make_tree(premise) == current:
                    response.is_valid = True
                    return response
        
            # If not found, invalid
            response.err_msg = "Expression on line {} not found in premises"\
                .format(str(current_line.line_no))
            return response

        except:
            response.err_msg = "One or more premises is invalid"
            return response