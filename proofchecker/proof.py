
class Proof:
    
    def __init__(self, lines=[]):
        self.lines = lines

class ProofLine:

    def __init__(self, line_no=None, formula=None, rule=None):
        self.line_no = line_no
        self.formula = formula
        self.rule = rule