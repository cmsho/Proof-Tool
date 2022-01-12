from proofchecker.proof import ProofObj, ProofLineObj, ProofResponse
from .rule import Rule

class Assumption(Rule):

    name = "Assumption"
    symbols = "Assumption"

    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        """
        Verify that an assumption is valid
        """
        response = ProofResponse()

        try:
            nums = str(current_line.line_no).replace('.', ' ')
            nums = nums.split()
            last_num = nums[len(nums)-1]

            # Assumptions should start a new subproof
            # (i.e. the last number in the line number should be '1')
            if str(last_num) == '1':
                response.is_valid = True
                return response
        
            response.err_msg = 'Assumptions can only exist at the start of a subproof'
            return response

        except:
            response.err_msg = 'One or more invalid line numbers.'
            return response