from Tree import Stmt

class SkipStmt(Stmt):
    def __init__(self):
        pass
    
    def wp(self, post):
        """The weakest precondition of skip is the postcondition.
        
        Args:
            post (Exp): Post condition
            
        Returns:
            Exp: The post condition (unchanged)
        """
        return post