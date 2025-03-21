from Tree import Stmt

class AssignStmt(Stmt):
    def __init__(self, var, exp):
        """Initialize an assignment statement.
        
        Args:
            var (Ident): The variable being assigned
            exp (Exp): The expression being assigned to the variable
        """
        self.var = var
        self.exp = exp
    
    def wp(self, post):
        """The weakest precondition of an assignment is the postcondition
        with all occurrences of the variable substituted with the expression.
        
        Args:
            post (Exp): Post condition
            
        Returns:
            Exp: The weakest precondition
        """
        # We need to substitute the variable with the expression in the postcondition
        return post.substitute(self.var.name, self.exp)