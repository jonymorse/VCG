import sys
from Tree import Exp

class Ident(Exp):
    def __init__(self, n):
        self.name = n

    def print(self):
        sys.stdout.write(self.name)
        
    def _print(self, parent, child):
        # Identifiers don't need parentheses regardless of operator precedence
        self.print()
        
    def substitute(self, var, exp):
        """Substitute var with exp if self.name matches var
        
        Returns:
            Exp: Either self or a copy of exp
        """
        # If this identifier matches the variable to be substituted,
        # return the substituting expression
        if self.name == var:
            return exp
        # Otherwise, return self unchanged
        return self