from Tree import Stmt, OpExp

class IfStmt(Stmt):
    def __init__(self, cond, then_stmt, else_stmt):
        """Initialize an if statement.
        
        Args:
            cond (Exp): The condition expression
            then_stmt (Stmt): The statement to execute if condition is true
            else_stmt (Stmt): The statement to execute if condition is false
        """
        self.cond = cond
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt
    
    def wp(self, post):
        """The weakest precondition of an if statement is:
        (cond => wp(then_stmt, post)) and (not cond => wp(else_stmt, post))
        
        Args:
            post (Exp): Post condition
            
        Returns:
            Exp: The weakest precondition
        """
        # Calculate wp for the then branch
        wp_then = self.then_stmt.wp(post)
        # Calculate wp for the else branch
        wp_else = self.else_stmt.wp(post)
        
        # Create the implication for the then branch: cond => wp_then
        imp_then = OpExp(self.cond, OpExp.Op.IMP, wp_then)
        
        # Create the negation of the condition: not cond
        not_cond = OpExp(None, OpExp.Op.NOT, self.cond)
        
        # Create the implication for the else branch: not cond => wp_else
        imp_else = OpExp(not_cond, OpExp.Op.IMP, wp_else)
        
        # Combine with AND: (cond => wp_then) and (not cond => wp_else)
        return OpExp(imp_then, OpExp.Op.AND, imp_else)