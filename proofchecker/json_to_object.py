import json


class ProofTemp:

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

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

#
#
class ProofLineTemp:

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

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

