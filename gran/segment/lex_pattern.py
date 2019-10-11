import re

class LexPattern:
    PAT_NONLITERAL = re.compile(r"[\(\[].*?[\)\]][?!+]?")

    @staticmethod
    def from_regex(pattern):
        lex_pat = LexPattern(pattern, True)
        return lex_pat

    def __init__(self, pattern, use_regex=False):
        self.__pattern = pattern
        self.__literals = None
        self.regex = None
        if use_regex:
            self.regex = re.compile(self.__pattern)

    def __repr__(self):
        return f"<LexPattern: {self.__pattern}>"
    @property
    def literals(self):
        if not self.__literals:
            self.literals = LexPattern.PAT_NONLITERAL.sub(self.__pattern, "")
        return self.__literals

    @property
    def pattern(self):
        return self.__pattern

    def prefix(self):
        if self.regex:
            return self.literals
        else:
            return self.__pattern[0]

    def findall(self, text):
        matches = []
        if self.regex:
            for mat in self.regex.finditer(text):
                mat_len = mat.end() - mat.start()
                matches.append((mat.start(), mat_len))
        else:
            midx = text.find(self.__pattern, 0)
            while midx >= 0:
                matches.append((midx, len(self.__pattern)))
                midx = text.find(self.__pattern, midx+1)
        return matches

