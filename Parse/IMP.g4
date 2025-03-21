grammar IMP;

@header {
from Tree import *
import sys
}

program
    : pre=assertion stmts=statementlist post=assertion
        {
try:
    # First calculate the main VC: pre => wp(stmt, post)
    wp = $stmts.stmt.wp($post.tree)
    main_vc = OpExp($pre.tree, OpExp.Op.IMP, wp)
    
    # Now collect any VCs from while loops
    vcs = []
    from Tree import collect_vcs
    collect_vcs($stmts.stmt, vcs)
    
    # For programs without loops, we just print the main VC
    # For programs with loops, print loop VCs first, then the main VC
    if not vcs:
        # Print the main VC
        main_vc.print()
        sys.stdout.write("\n")
    else:
        # Print the loop VCs in the required order:
        # 1. Loop exit condition
        # 2. Loop preservation
        for vc in vcs:
            vc.print()
            sys.stdout.write("\n")
        
        # Then print the main VC
        main_vc.print()
        sys.stdout.write("\n")
    
    sys.stdout.flush()
except Exception as e:
    sys.stderr.write(f"Error: {str(e)}\n")
        }
    ;

statementlist returns [Stmt stmt]
    : s=statement
        {$stmt = $s.stmt}
    | s1=statement ';' s2=statementlist
        {$stmt = SeqStmt($s1.stmt, $s2.stmt)}
    ;

statement returns [Stmt stmt]
    : 'skip'
        {$stmt = SkipStmt()}
    | ident_var=ident ':=' exp=arithexp
        {$stmt = AssignStmt($ident_var.name, $exp.tree)}
    | 'begin' stmts=statementlist 'end'
        {$stmt = BlockStmt($stmts.stmt)}
    | 'if' cond=boolterm 'then' then_stmt=statement 'else' else_stmt=statement
        {$stmt = IfStmt($cond.tree, $then_stmt.stmt, $else_stmt.stmt)}
    | inv=assertion 'while' cond=boolterm 'do' body=statement
        {$stmt = WhileStmt($cond.tree, $body.stmt, $inv.tree)}
    | 'assert' a=assertion
        {$stmt = AssertStmt($a.tree)}
    ;

assertion returns [Exp tree]
    : '{' t=boolexp '}'
        {$tree = $t.tree}
    ;

boolexp returns [Exp tree]
    : t=boolterm
        {$tree = $t.tree}
    | t1=boolterm '=>' t2=boolterm
        {$tree = OpExp($t1.tree, OpExp.Op.IMP, $t2.tree)}
    | t1=boolterm '<=>' t2=boolterm
        {$tree = OpExp($t1.tree, OpExp.Op.EQV, $t2.tree)}
    ;

boolterm returns [Exp tree]
    : t=boolterm2
        {$tree = $t.tree}
    | t1=boolterm 'or' t2=boolterm2
        {$tree = OpExp($t1.tree, OpExp.Op.OR, $t2.tree)}
    ;

boolterm2 returns [Exp tree]
    : t=boolfactor
        {$tree = $t.tree}
    | t1=boolterm2 'and' t2=boolfactor
        {$tree = OpExp($t1.tree, OpExp.Op.AND, $t2.tree)}
    ;

boolfactor returns [Exp tree]
    : 'true'
        {$tree = BoolLit(True)}
    | 'false'
        {$tree = BoolLit(False)}
    | c=compexp
        {$tree = $c.tree}
    | 'forall' ident_var=ident '.' b=boolexp
        {$tree = OpExp($ident_var.name, OpExp.Op.FORALL, $b.tree)}
    | 'exists' ident_var=ident '.' b=boolexp
        {$tree = OpExp($ident_var.name, OpExp.Op.EXISTS, $b.tree)}
    | 'not' bf=boolfactor
        {$tree = OpExp(None, OpExp.Op.NOT, $bf.tree)}
    | '(' t=boolexp ')'
        {$tree = $t.tree}
    ;

compexp returns [Exp tree]
    : t1=arithexp '<' t2=arithexp
        {$tree = OpExp($t1.tree, OpExp.Op.LT, $t2.tree)}
    | t1=arithexp '<=' t2=arithexp
        {$tree = OpExp($t1.tree, OpExp.Op.LE, $t2.tree)}
    | t1=arithexp '=' t2=arithexp
        {$tree = OpExp($t1.tree, OpExp.Op.EQ, $t2.tree)}
    | t1=arithexp '!=' t2=arithexp
        {$tree = OpExp($t1.tree, OpExp.Op.NE, $t2.tree)}
    | t1=arithexp '>=' t2=arithexp
        {$tree = OpExp($t1.tree, OpExp.Op.GE, $t2.tree)}
    | t1=arithexp '>' t2=arithexp
        {$tree = OpExp($t1.tree, OpExp.Op.GT, $t2.tree)}
    ;

arithexp returns [Exp tree]
    : t=arithterm
        {$tree = $t.tree}
    | t1=arithexp '+' t2=arithterm
        {$tree = OpExp($t1.tree, OpExp.Op.PLUS, $t2.tree)}
    | t1=arithexp '-' t2=arithterm
        {$tree = OpExp($t1.tree, OpExp.Op.MINUS, $t2.tree)}
    ;

arithterm returns [Exp tree]
    : t=arithfactor
        {$tree = $t.tree}
    | t1=arithterm '*' t2=arithfactor
        {$tree = OpExp($t1.tree, OpExp.Op.TIMES, $t2.tree)}
    | t1=arithterm '/' t2=arithfactor
        {$tree = OpExp($t1.tree, OpExp.Op.DIV, $t2.tree)}
    ;

arithfactor returns [Exp tree]
    : ident_var=ident
        {$tree = $ident_var.name}
    | i=integer
        {$tree = $i.value}
    | '-' af=arithfactor
        {$tree = OpExp(None, OpExp.Op.UMINUS, $af.tree)}
    | '(' t=arithexp ')'
        {$tree = $t.tree}
    | ident_var=ident '(' args=arithexplist ')'
        {$tree = FuncExp($ident_var.name, $args.explist)}
    ;

arithexplist returns [list explist]
    : exp=arithexp
        {$explist = [$exp.tree]}
    | exp=arithexp ',' rest=arithexplist
        {$explist = [$exp.tree] + $rest.explist}
    ;

ident returns [Ident name]
    : IDENT
        {$name = Ident($IDENT.text)}
    ;

integer returns [IntLit value]
    : INT
        {$value = IntLit(int($INT.text))}
    ;

IDENT
    : [A-Za-z][A-Za-z0-9_]*
    ;

INT
    : [0]|[1-9][0-9]*
    ;

WS
    : [ \r\n\t] -> skip
    ;