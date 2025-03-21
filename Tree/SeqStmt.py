from Tree import Stmt

class SeqStmt(Stmt):
    def __init__(self, s1, s2):
        """Initialize a sequence of statements.
        
        Args:
            s1 (Stmt): The first statement
            s2 (Stmt): The second statement
        """
        self.s1 = s1
        self.s2 = s2
    
    def wp(self, post):
        """The weakest precondition of a sequence is the weakest precondition of
        the first statement with respect to the weakest precondition of the second.
        
        Args:
            post (Exp): Post condition
            
        Returns:
            Exp: The weakest precondition
        """
        # First calculate wp of the second statement
        wp_s2 = self.s2.wp(post)
        # Then calculate wp of the first statement with respect to wp_s2
        return self.s1.wp(wp_s2)