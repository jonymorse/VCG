from Tree import Stmt, OpExp

class AssertStmt(Stmt):
    def __init__(self, assertion):
        """Initialize an assert statement.
        
        Args:
            assertion (Exp): The assertion expression
        """
        self.assertion = assertion
    
    def wp(self, post):
        """The weakest precondition of an assert statement is:
        assertion and (assertion => post)
        
        Args:
            post (Exp): Post condition
            
        Returns:
            Exp: The weakest precondition
        """
        # Create the implication: assertion => post
        imp = OpExp(self.assertion, OpExp.Op.IMP, post)
        
        # Combine with AND: assertion and (assertion => post)
        return OpExp(self.assertion, OpExp.Op.AND, imp)