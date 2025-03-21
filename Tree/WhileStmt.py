from Tree import Stmt, OpExp

class WhileStmt(Stmt):
    def __init__(self, cond, body, inv):
        """Initialize a while statement.
        
        Args:
            cond (Exp): The loop condition
            body (Stmt): The loop body
            inv (Exp): The loop invariant
        """
        self.cond = cond
        self.body = body
        self.inv = inv
        self.vcs = []  # List to store verification conditions
    
    def wp(self, post):
        """For while loops, we don't combine verification conditions.
        Instead, we generate three verification conditions:
        1. inv and not cond => post (loop exit)
        2. inv and cond => wp(body, inv) (loop preservation)
        3. Return the invariant as the weakest precondition
        
        Args:
            post (Exp): Post condition
            
        Returns:
            Exp: The loop invariant
        """
        # Clear previous VCs if any
        self.vcs = []
        
        # 1. Loop exit condition: inv and not cond => post
        not_cond = OpExp(None, OpExp.Op.NOT, self.cond)
        inv_and_not_cond = OpExp(self.inv, OpExp.Op.AND, not_cond)
        exit_vc = OpExp(inv_and_not_cond, OpExp.Op.IMP, post)
        self.vcs.append(exit_vc)
        
        # 2. Loop preservation: inv and cond => wp(body, inv)
        wp_body = self.body.wp(self.inv)
        inv_and_cond = OpExp(self.inv, OpExp.Op.AND, self.cond)
        preservation_vc = OpExp(inv_and_cond, OpExp.Op.IMP, wp_body)
        self.vcs.append(preservation_vc)
        
        # 3. Return the invariant as the weakest precondition
        return self.inv
    
    def get_vcs(self):
        """Get the verification conditions for this while loop.
        
        Returns:
            list: List of verification conditions
        """
        return self.vcs