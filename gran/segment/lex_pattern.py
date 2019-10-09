import re

class LexPattern:
    PAT_NONLITERAL = re.compile(r"[\(\[].*?[\)\]][?!+]?")
    def __init__(self, pattern):
        self.pattern = pattern
        self.regex = None
        self.literals = None

    @property
    def literals(self):
        if not self.literals:
            self.literals = LexPattern.PAT_NONLITERAL.sub(self.pattern, "")
        return self.literals
    
    def findall(self, text):
        if not self.regex:
            self.regex = re.compile(self.pattern)        
        matches = []
        for mat in self.regex.finditer(text):
            matches.append((mat.start(), mat.end(), mat.group()))
        return matches
        

