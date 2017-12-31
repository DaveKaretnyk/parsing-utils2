## Parsing utilities, experiments, and test code

### Introduction / Purpose
This repository contains code (e.g test programs) that I developed while experimenting with the
ATNLR parser from Terence Parr.

    <http://www.antlr.org/>
    <https://github.com/antlr>
    
Maybe there is something in here that is useful to others... Feel free to have a look and let me
know what you think. As you will see there are plenty of things that could be improved! lol
For me it is just a matter or priorities, so I'm making what I have available at is currently
stands.

I work in software development during the day and originally graduated in Computer Science a long
time ago (mid 80's) when we did not really know what Computer Science or Software Engineering was.
Interestingly in many ways it seems that we still do not know ;-)

I vaguely recall Lex and Yacc as an undergraduate student and like most found them a bit esoteric
and just plain difficult to use. Not for me was the conclusion. Roll forward 30+ years (geez) to
find life has gotten easier.

I understand one of the goals of ANTLR is to make the use of lexing and parsing techniques more
accessible to 'normal developers'? That is, people who are primarily working in different areas
but might make sensible use of parsing techniques as part of an overall problem solution? If so
then hats off - mission accomplished. The ANTLR book (The Definitive ANTLR 4 Reference) does an
excellent job of explaining the what, why, and how right from the very basics. And to be honest I
spent probably more time figuring out the details of Java and IntelliJ IDEA (both new to me) than I
I did figuring out ANTLR concepts.

The pdf in the 'docs' directory is a little poster that I prepared for colleagues a while back to
try and explain why I thought this parsing stuff is worth taking a fresh look at.

###Index to Content
A short description here of the purpose of each directory (typically a directory contains a
project of some description).

#### check-python-33-manual
Program that scans Python modules (files) or packages (directories) for 3.3 syntax and flags any
detected errors. This uses the Python 3.3 grammar from Bart Kiers:

    <https://github.com/bkiers/python3-parser>

In that respect then nothing new, just my own experimenting to get started with ANTLR, and Java...
 and IntelliJ IDEA... More information in the readme.txt in the directory.

#### check-python-27-manual
Program that scans Python modules (files) or packages (directories) for 2.7 syntax and flags any
detected errors.

The grammar was developed by taking the 3.3 grammar from Kiers as starting point. Then diffing the
official Python 2.7 grammar specification against the 3.3 specification to figure out what changes
were needed. More information in the readme.txt in the directory.
