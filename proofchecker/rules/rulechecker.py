from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj
from proofchecker.rules.assumption import Assumption
from proofchecker.rules.biconditionalelim import BiconditionalElim
from proofchecker.rules.biconditionalintro import BiconditionalIntro
from proofchecker.rules.conditionalelim import ConditionalElim
from proofchecker.rules.conditionalintro import ConditionalIntro
from proofchecker.rules.conjunctionelim import ConjunctionElim
from proofchecker.rules.conjunctionintro import ConjunctionIntro
from proofchecker.rules.demorgan import DeMorgan
from proofchecker.rules.disjunctionelim import DisjunctionElim
from proofchecker.rules.disjunctionintro import DisjunctionIntro
from proofchecker.rules.disjunctivesyllogism import DisjunctiveSyllogism
from proofchecker.rules.doublenegationelim import DoubleNegationElim
from proofchecker.rules.excludedmiddle import ExcludedMiddle
from proofchecker.rules.explosion import Explosion
from proofchecker.rules.indirectproof import IndirectProof
from proofchecker.rules.modustollens import ModusTollens
from proofchecker.rules.negationelim import NegationElim
from proofchecker.rules.negationintro import NegationIntro
from proofchecker.rules.premise import Premise
from proofchecker.rules.reiteration import Reiteration
from .rule import Rule


TFL_BASIC_RULES = [Premise(), Assumption(), ConjunctionIntro(), ConjunctionElim(), DisjunctionIntro(), DisjunctionElim(), \
    ConditionalIntro(), ConditionalElim(), BiconditionalIntro(), BiconditionalElim(), NegationIntro(), NegationElim(), \
    Explosion(), IndirectProof()]

TFL_DERIVED_RULES = [DisjunctiveSyllogism(), ModusTollens(), DoubleNegationElim(), Reiteration(), ExcludedMiddle(), DeMorgan()]

class RuleChecker:

    def get_rule(self, rule: str):
        """
        Determine which rule is being applied
        """

        for basic_rule in TFL_BASIC_RULES:
            if rule.casefold() == basic_rule.symbols.casefold():
                return basic_rule

        for derived_rule in TFL_DERIVED_RULES:
            if rule.casefold() == derived_rule.symbols.casefold():
                return derived_rule
        
        return None