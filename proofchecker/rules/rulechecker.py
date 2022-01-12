from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj
from proofchecker.rules.assumption import Assumption
from proofchecker.rules.biconditionalelim import BiconditionalElim
from proofchecker.rules.biconditionalintro import BiconditionalIntro
from proofchecker.rules.conditionalelim import ConditionalElim
from proofchecker.rules.conditionalintro import ConditionalIntro
from proofchecker.rules.conjunctionelim import ConjunctionElim
from proofchecker.rules.conjunctionintro import ConjunctionIntro
from proofchecker.rules.disjunctionelim import DisjunctionElim
from proofchecker.rules.disjunctionintro import DisjunctionIntro
from proofchecker.rules.doublenegationelim import DoubleNegationElim
from proofchecker.rules.explosion import Explosion
from proofchecker.rules.indirectproof import IndirectProof
from proofchecker.rules.negationelim import NegationElim
from proofchecker.rules.negationintro import NegationIntro
from proofchecker.rules.premise import Premise
from proofchecker.rules.reiteration import Reiteration
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

    def get_rule(self, rule: str):
        """
        Determine which rule is being applied
        """
        if rule.casefold() == 'premise':
            return Premise()
        elif (rule.casefold() == 'assumption') or (rule.casefold() == 'assumpt'):
            return Assumption()
        elif rule.casefold() == 'x':
            return Explosion()
        elif rule.casefold() == 'r':
            return Reiteration()
        elif rule.casefold() == 'dne':
            return DoubleNegationElim()
        elif rule.casefold() == '∧i':
            return ConjunctionIntro()
        elif rule.casefold() == '∧e':
            return ConjunctionElim()
        elif rule.casefold() == '∨i':
            return DisjunctionIntro()
        elif rule.casefold() == '∨e':
            return DisjunctionElim()
        elif rule.casefold() == '¬i':
            return NegationIntro()
        elif rule.casefold() == '¬e':
            return NegationElim()
        elif rule.casefold() == '→i':
            return ConditionalIntro()
        elif rule.casefold() == '→e':
            return ConditionalElim()
        elif rule.casefold() == 'ip':
            return IndirectProof()
        elif rule.casefold() == '↔i':
            return BiconditionalIntro()
        elif rule.casefold() == '↔e':
            return BiconditionalElim()
        
        return None