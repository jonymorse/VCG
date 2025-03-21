import sys
from Tree import Exp

class IntLit(Exp):
    def __init__(self, v):
        self.value = v

    def print(self):
        sys.stdout.write(str(self.value))
        
    def _print(self, parent, child):
        # Integer literals don't need parentheses regardless of operator precedence
        self.print()
        
    def substitute(self, var, exp):
        """Substitute operation for integer literals.
        
        Since integer literals don't contain variables, this just returns self.
        
        Returns:
            Exp: self unchanged
        """
        # Integer literals don't contain variables, so no substitution needed
        return self