# Makefile for the CSC 7101 Verification Condition Generator

MAIN = VCG
LANG = IMP
PDIR = Parse
TDIR = Tree
SRC  = ${PDIR} ${TDIR} ${MAIN}.py

ANTLR= antlr-4.9.2-complete.jar

ARUN = java -jar ${ANTLR}

all: antlr
	python3 -m compileall ${SRC}

antlr: ${PDIR}/${LANG}.g4
	(cd ${PDIR}; ${ARUN} -Dlanguage=Python3 ${LANG}.g4)

clean:
	rm -rf __pycache__ *~ ${TDIR}/__pycache__ ${TDIR}/*~
	(cd ${PDIR}; rm -rf ${LANG}*.py ${LANG}*.tokens *.interp __pycache__ *~)
