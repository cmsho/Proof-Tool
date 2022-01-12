from proofchecker.proof import ProofObj, ProofLineObj, ProofResponse
from .rule import Rule

class RuleChecker:
    """
    Client interface for checking if a rule is valid.
    Maintains a reference to the instance of a Rule subclass.
    """

    _rule = None
    """
    A reference to the current state of the delegate
    """

    def __init(self, rule: Rule) -> None:
        self

    def set_rule(self, rule: Rule):
        """
        The context allows changing the Rule object at runtime
        """
        self._rule = rule
    
    """
    The context delegates part of its behavior to the current Rule object
    """

    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        """
        Verify if the rule is applied correctly
        """
        self._rule.verify()