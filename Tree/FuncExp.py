import sys
from Tree import Exp

class FuncExp(Exp):
    def __init__(self, name, args):
        self.name = name  # The function identifier (Ident)
        self.args = args  # List of argument expressions
        
    def print(self):
        self.name.print()
        sys.stdout.write("(")
        for i, arg in enumerate(self.args):
            if i > 0:
                sys.stdout.write(", ")
            arg.print()
        sys.stdout.write(")")
        
    def _print(self, parent, child):
        # Function calls don't need parentheses regardless of operator precedence
        self.print()
        
    def substitute(self, var, exp):
        """Substitute var with exp in this function call.
        
        Args:
            var (str): Variable name to be substituted
            exp (Exp): Expression to substitute with
            
        Returns:
            Exp: A new function call expression with the substitution applied
        """
        # Substitute in the function name (if it's an identifier)
        new_name = self.name.substitute(var, exp)
        
        # Substitute in all arguments
        new_args = [arg.substitute(var, exp) for arg in self.args]
        
        return FuncExp(new_name, new_args)