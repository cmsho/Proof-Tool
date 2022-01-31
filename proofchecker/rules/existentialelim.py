from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from .rule import Rule

class ExistentialElim(Rule):

    name = "Existential Elimination"
    symbols = "∃E"

    
    def verify(self, current_line: ProofLineObj, proof: ProofObj, parser):
        """
        Verify proper impelmentation of the rule ∃E m
        (Existential Elimination)
        """
        pass