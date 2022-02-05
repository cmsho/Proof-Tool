from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from .rule import Rule

class UniversalElim(Rule):

    name = "Universal Elimination"
    symbols = "∀I"

    def verify(self, current_line: ProofLineObj, proof: ProofObj, parser):
        """
        Verify proper impelmentation of the rule ∀E I
        (Universal Elimination)
        """
        pass