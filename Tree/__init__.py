from Tree.Exp import Exp
from Tree.Ident import Ident
from Tree.IntLit import IntLit
from Tree.BoolLit import BoolLit
from Tree.OpExp import OpExp
from Tree.FuncExp import FuncExp

from Tree.Stmt import Stmt
from Tree.SkipStmt import SkipStmt
from Tree.AssignStmt import AssignStmt
from Tree.SeqStmt import SeqStmt
from Tree.IfStmt import IfStmt
from Tree.WhileStmt import WhileStmt
from Tree.AssertStmt import AssertStmt
from Tree.BlockStmt import BlockStmt

def collect_vcs(stmt, vcs):
    """Recursively collect verification conditions from the statement tree."""
    if isinstance(stmt, WhileStmt):
        # We need to make sure we don't pass None as the post-condition
        # Use the loop invariant as a dummy post-condition if needed
        wp = stmt.wp(stmt.inv)  # This will populate stmt.vcs with the right VCs
        vcs.extend(stmt.get_vcs())
        
        # Check the body for nested while statements
        collect_vcs(stmt.body, vcs)
    elif isinstance(stmt, SeqStmt):
        # Check both sides of the sequence
        collect_vcs(stmt.s1, vcs)
        collect_vcs(stmt.s2, vcs)
    elif isinstance(stmt, IfStmt):
        # Check both branches
        collect_vcs(stmt.then_stmt, vcs)
        collect_vcs(stmt.else_stmt, vcs)
    elif isinstance(stmt, BlockStmt):
        # Check the statement inside the block
        collect_vcs(stmt.stmt, vcs)

__all__ = [
    "Exp", "Ident", "IntLit", "BoolLit", "OpExp", "FuncExp",
    "Stmt", "SkipStmt", "AssignStmt", "SeqStmt", "IfStmt", 
    "WhileStmt", "AssertStmt", "BlockStmt", "collect_vcs"
]