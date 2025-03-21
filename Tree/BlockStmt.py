from Tree import Stmt

class BlockStmt(Stmt):
    def __init__(self, stmt):
        """Initialize a block statement (begin ... end).
        
        Args:
            stmt (Stmt): The statement inside the block
        """
        self.stmt = stmt
    
    def wp(self, post):
        """The weakest precondition of a block is the weakest precondition of
        the enclosed statement.
        
        Args:
            post (Exp): Post condition
            
        Returns:
            Exp: The weakest precondition
        """
        return self.stmt.wp(post)