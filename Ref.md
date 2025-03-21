cs710118@classes:~/prog1$ cd Parse
cs710118@classes:~/prog1/Parse$ java -jar antlr-4.9.2-complete.jar -Dlanguage=Python3 IMP.g4
cs710118@classes:~/prog1/Parse$ cd ..
cs710118@classes:~/prog1$ python3 -m compileall Parse Tree VCG.py
Listing 'Parse'...
Compiling 'Parse/IMPLexer.py'...
Compiling 'Parse/IMPListener.py'...
Compiling 'Parse/IMPParser.py'...
Compiling 'Parse/__init__.py'...
Listing 'Tree'...
Compiling 'Tree/Exp.py'...
Compiling 'Tree/Ident.py'...
Compiling 'Tree/IntLit.py'...
Compiling 'Tree/OpExp.py'...
Compiling 'Tree/__init__.py'...
Compiling 'VCG.py'...
cs710118@classes:~/prog1$ tree
.
├── intdiv.vcg
├── Makefile
├── Parse
│   ├── antlr-4.13.2-complete.jar
│   ├── antlr-4.9.2-complete.jar
│   ├── IMP.g4
│   ├── IMP.interp
│   ├── IMPLexer.interp
│   ├── IMPLexer.py
│   ├── IMPLexer.tokens
│   ├── IMPListener.py
│   ├── IMPParser.py
│   ├── IMP.tokens
│   ├── __init__.py
│   └── __pycache__
│       ├── IMPLexer.cpython-311.pyc
│       ├── IMPListener.cpython-311.pyc
│       ├── IMPParser.cpython-311.pyc
│       └── __init__.cpython-311.pyc
├── __pycache__
│   └── VCG.cpython-311.pyc
├── README.md
├── test.svg
├── test.vcg
├── Tree
│   ├── Exp.py
│   ├── Ident.py
│   ├── __init__.py
│   ├── IntLit.py
│   ├── OpExp.py
│   └── __pycache__
│       ├── Exp.cpython-311.pyc
│       ├── Ident.cpython-311.pyc
│       ├── __init__.cpython-311.pyc
│       ├── IntLit.cpython-311.pyc
│       └── OpExp.cpython-311.pyc
├── VCG18.jar
└── VCG.py

6 directories, 33 files
cs710118@classes:~/prog1$ awk 'FNR==1{print "File: " FILENAME "\n"} {print}' Tree/*.py
File: Tree/Exp.py

from abc import ABC, abstractmethod

class Exp(ABC):
    @abstractmethod
    def print(self):
        pass

    def _print(self, parent, child):
        self.print()
File: Tree/Ident.py

import sys
from Tree import Exp

class Ident(Exp):
    def __init__(self, n):
        self.name = n

    def print(self):
        sys.stdout.write(self.name)
File: Tree/__init__.py

from Tree.Exp import Exp
from Tree.Ident import Ident
from Tree.IntLit import IntLit
from Tree.OpExp import OpExp

__all__ = ["Exp", "Ident", "IntLit", "OpExp"]
File: Tree/IntLit.py

import sys
from Tree import Exp

class IntLit(Exp):
    def __init__(self, v):
        self.value = v

    def print(self):
        sys.stdout.write(str(self.value))
File: Tree/OpExp.py

import sys
from enum import Enum
from enum import IntEnum
from Tree import Exp

class OpExp(Exp):
    class Op(IntEnum):
        IMP = 0
        EQV = 1
        OR = 2
        AND = 3
        NOT = 4
        LT = 5
        LE = 6
        EQ = 7
        NE = 8
        GT = 9
        GE = 10
        PLUS = 11
        MINUS = 12
        TIMES = 13
        DIV = 14
        UMINUS = 15

    class LR(Enum):
        LEFT = 0
        RIGHT = 1

    __opnames = [" => ", " <=> ", " or ", " and ", "not ",
                 "<", "<=", "=", "!=", ">", ">=",
                 "+", "-", "*", "/", "-"]
    
    __precedence = [2, 2, 3, 4, 5,
                    6, 6, 6, 6, 6, 6,
                    7, 7, 8, 8, 9]
    
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

cs710118@classes:~/prog1$ cat VCG.py 
#!/usr/bin/python3

import sys
from antlr4 import *
from Parse import *
from Tree import *


def main(argv):
    if (len(argv) != 2):
        sys.stderr.write("Usage: python3 VCG.py test.vcg\n")
        sys.exit(1)

    input = FileStream(argv[1])
    lexer = IMPLexer(input)
    tokens = CommonTokenStream(lexer)
    parser = IMPParser(tokens)

    parser.program()


if __name__ == "__main__":
    main(sys.argv)
cs710118@classes:~/prog1$ cat Parse/IMP.g4 
grammar IMP;

@header {
from Tree import *
}

program
    : pre=assertion statementlist post=assertion
                {
# FIXME: Construct and print verification condition instead
$pre.tree.print()
sys.stdout.write("\n")
$post.tree.print()
sys.stdout.write("\n")
sys.stdout.flush()
                }
    ;

statementlist
    : statement
    | statement ';' statementlist
    ;

statement
    : 'skip'
    | ident ':=' arithexp
    | 'begin' statementlist 'end'
    | 'if' boolterm 'then' statement 'else' statement
    | assertion 'while' boolterm 'do' statement
    | 'assert' assertion
    ;

assertion returns [Exp tree]
    : '{' t=boolexp '}'
                {$tree = $t.tree}
    ;

boolexp returns [Exp tree]
    : t=boolterm
                {$tree = $t.tree}
    | boolterm '=>' boolterm
    | boolterm '<=>' boolterm
    ;

boolterm returns [Exp tree]
    : t=boolterm2
                {$tree = $t.tree}
    | boolterm 'or' boolterm2
    ;

boolterm2 returns [Exp tree]
    : t=boolfactor
                {$tree = $t.tree}
    | boolterm2 'and' boolfactor
    ;

boolfactor returns [Exp tree]
    : 'true'
    | 'false'
    | compexp
                {$tree = $compexp.tree}
    | 'forall' ident '.' boolexp
    | 'exists' ident '.' boolexp
    | 'not' boolfactor
    | '(' t=boolexp ')'
                {$tree = $t.tree}
    ;

compexp returns [Exp tree]
    : arithexp '<' arithexp
    | arithexp '<=' arithexp
    | t1=arithexp '=' t2=arithexp
                {$tree = OpExp($t1.tree, OpExp.Op.EQ, $t2.tree)}
    | arithexp '!=' arithexp
    | arithexp '>=' arithexp
    | arithexp '>' arithexp
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
    : ident
                {$tree = $ident.name}
    | integer
                {$tree = $integer.value}
    | '-' arithfactor
    | '(' t=arithexp ')'
                {$tree = $t.tree}
    | ident '(' arithexplist ')'
    ;

arithexplist
    : arithexp
    | arithexp ',' arithexplist
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
cs710118@classes:~/prog1$ 