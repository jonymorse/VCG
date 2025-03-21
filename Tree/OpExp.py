import sys
from enum import Enum
from enum import IntEnum
from Tree import Exp

class OpExp(Exp):
    class Op(IntEnum):
        IMP = 0    # =>
        EQV = 1    # <=>
        OR = 2
        AND = 3
        NOT = 4
        LT = 5     # 
        LE = 6     # <=
        EQ = 7     # =
        NE = 8     # !=
        GT = 9     # >
        GE = 10    # >=
        PLUS = 11  # +
        MINUS = 12 # -
        TIMES = 13 # *
        DIV = 14   # /
        UMINUS = 15 # unary -
        FORALL = 16 # forall quantifier
        EXISTS = 17 # exists quantifier

    class LR(Enum):
        LEFT = 0
        RIGHT = 1

    __opnames = [" => ", " <=> ", " or ", " and ", "not ",
                 "<", "<=", "=", "!=", ">", ">=",
                 "+", "-", "*", "/", "-", 
                 "forall ", "exists "]
    
    __precedence = [2, 2, 3, 4, 5,
                    6, 6, 6, 6, 6, 6,
                    7, 7, 8, 8, 9,
                    1, 1]  # Quantifiers have lowest precedence
    
    def __init__(self, l, o, r):
        self.left = l
        self.op = o
        self.right = r

    def print(self):
        if self.left != None:
            self.left._print(self.op, OpExp.LR.LEFT)
        sys.stdout.write(OpExp.__opnames[int(self.op)])
        self.right._print(self.op, OpExp.LR.RIGHT)

    def _print(self, parent, child):
        if (OpExp.__precedence[int(parent)]>OpExp.__precedence[int(self.op)] or
                (child==OpExp.LR.RIGHT and parent==OpExp.Op.MINUS and
                 self.op==OpExp.Op.MINUS)):
            sys.stdout.write('(')
            self.print()
            sys.stdout.write(')')
        else:
            self.print()
            
    def substitute(self, var, exp):
        """Substitute var with exp in this expression.
        
        Args:
            var (str): Variable name to be substituted
            exp (Exp): Expression to substitute with
            
        Returns:
            Exp: A new expression with the substitution applied
        """
        # For unary operations like NOT and UMINUS
        if self.left is None:
            # Only substitute in the right operand
            new_right = self.right.substitute(var, exp)
            return OpExp(None, self.op, new_right)
        
        # For quantified expressions (FORALL, EXISTS)
        if self.op == OpExp.Op.FORALL or self.op == OpExp.Op.EXISTS:
            # Check if the bound variable is the same as the substitution variable
            if isinstance(self.left, Ident) and self.left.name == var:
                # If the bound variable is the same as the substitution variable,
                # don't substitute inside the scope of the quantifier
                return self
            else:
                # Otherwise, substitute in the right operand (body of quantifier)
                new_right = self.right.substitute(var, exp)
                return OpExp(self.left, self.op, new_right)
        
        # For binary operations
        new_left = self.left.substitute(var, exp)
        new_right = self.right.substitute(var, exp)
        return OpExp(new_left, self.op, new_right)