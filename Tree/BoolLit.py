import sys
from Tree import Exp

class BoolLit(Exp):
    def __init__(self, v):
        self.value = v

    def print(self):
        if self.value:
            sys.stdout.write("true")
        else:
            sys.stdout.write("false")
            
    def _print(self, parent, child):
        # Boolean literals don't need parentheses regardless of operator precedence
        self.print()
        
    def substitute(self, var, exp):
        """Substitute operation for boolean literals.
        
        Since boolean literals don't contain variables, this just returns self.
        
        Returns:
            Exp: self unchanged
        """
        # Boolean literals don't contain variables, so no substitution needed
        return self