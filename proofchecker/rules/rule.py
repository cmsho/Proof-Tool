from abc import ABC, abstractmethod
from proofchecker.proof import ProofObj, ProofLineObj

class Rule(ABC):
    """
    An interface for creating Rule objects
    """

    @abstractmethod
    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        pass