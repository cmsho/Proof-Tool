# Objects
class ProofObj:
    
    def __init__(self, premises=[], conclusion='', lines=[], created_by=''):
        self.premises = premises
        self.conclusion = conclusion
        self.lines = lines
        self.created_by = created_by
    
    def __str__(self):
        result = ''
        for line in self.lines:
            result += str(line) +'\n'
        return result

    def __iter__(self):
        return (x for x in self.lines)

class ProofLineObj:

    def __init__(self, line_no=None, expression=None, rule=None):
        self.line_no = line_no
        self.expression = expression
        self.rule = rule
    
    def __str__(self):
        return ('Line {}: {}, {}'.format(
            self.line_no,
            self.expression,
            self.rule
        ))

class ProofResponse:

    def __init__(self, is_valid=False, err_msg=None):
        self.is_valid = is_valid
        self.err_msg = err_msg