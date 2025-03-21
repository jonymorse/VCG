# Verification Condition Generator (VCG) for IMP Language

## Jonathan Morse

## Overview
This project implements a Verification Condition Generator for the IMP language using the Weakest Precondition Predicate Transformer semantics. The VCG takes a Hoare triple as input and generates verification conditions that need to be satisfied for the program to be correct.

## Implementation Details

### Expression Tree Classes
The expression tree is implemented using the Composite Design Pattern, with an abstract `Exp` class and concrete subclasses for different types of expressions:

- `Exp`: Abstract base class for all expressions
- `Ident`: Represents an identifier (variable)
- `IntLit`: Represents an integer literal
- `BoolLit`: Represents a boolean literal (true/false)
- `OpExp`: Represents operations (arithmetic, logical, relational)
- `FuncExp`: Represents function calls

All expression classes implement:
- `print()`: Prints the expression
- `_print()`: Helper method for handling precedence during printing
- `substitute(var, exp)`: Substitutes all occurrences of variable `var` with expression `exp`

### Statement Tree Classes
The statement hierarchy includes:

- `Stmt`: Abstract base class for all statements
- `SkipStmt`: Represents the skip statement (no-op)
- `AssignStmt`: Represents an assignment statement
- `SeqStmt`: Represents a sequence of statements
- `IfStmt`: Represents an if-then-else statement
- `WhileStmt`: Represents a while loop with an invariant
- `AssertStmt`: Represents an assertion
- `BlockStmt`: Represents a block of statements (begin/end)

Each statement class implements a `wp(post)` method to calculate its weakest precondition with respect to a given postcondition.

### Weakest Precondition Calculation
The implementation follows the standard rules for weakest precondition calculation:

- Skip: wp(skip, Q) = Q
- Assignment: wp(x := e, Q) = Q[x/e] (substitution of x with e in Q)
- Sequence: wp(S1; S2, Q) = wp(S1, wp(S2, Q))
- If: wp(if B then S1 else S2, Q) = (B ⇒ wp(S1, Q)) ∧ (¬B ⇒ wp(S2, Q))
- While: For loops, we generate specific verification conditions:
  1. (inv ∧ ¬cond) ⇒ post (loop exit)
  2. (inv ∧ cond) ⇒ wp(body, inv) (loop preservation)

### Grammar and Parsing
The project uses ANTLR to define the grammar for the IMP language and to generate a parser. The parser builds expression and statement trees, which are then used to compute verification conditions.

### Handling Verification Conditions
The program generates and prints verification conditions in the required format:
- For simple programs (without loops), it prints a single VC
- For programs with loops, it prints multiple VCs in the required order:
  1. Loop exit condition
  2. Loop preservation condition
  3. Main verification condition

## Usage
To compile and run the VCG:
cd ~/prog1
make
python3 VCG.py <input_file>
