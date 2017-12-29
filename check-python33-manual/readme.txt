Grammar checker for Python modules
----------------------------------
Check the grammar of the specified Python modules (files).

Main features:
    + Client can specify either a single module (.py file) or list of modules
     (directory).
	+ JUnit tests for a few miscellaneous files and for a snapshot of the
	  3.3.7 standard library sources.
	+ Handle UTF-8 BOM marker in files - that tripped me up for a while.

With respect to grammar, this is the same Python 3.3 grammar that you will
find from Bart Kiers @
	https://github.com/bkiers/python3-parser
In that respect then nothing new, just my own experimenting to get started
with ANTLR (and Java).

Setup
-----
Manual setup within IntelliJ IDEA using the ANTLR plugin to configure how
grammar files are generated. Not the best organization, but useful as a
starting point to understand what is going on.

Same structure as the checker that was developed for Python 2.7. This was done
to give a reference point since the ANTLR 3.3 grammar is the what the 2.7
grammar was originally developed from. See directory 'check-python27-manual'.

Manual setup:
1. Assuming the ANTLR IntelliJ IDEA plugin in installed.
2. Create an IntelliJ project (type just 'plain Java') for the sources of this
   directory.
3. Bring up the 'Configure ANTLR...' dialog (right click on the .g4 file in
   the IntelliJ editor.
   a. Set the 'Output directory to where all output is generated' to the root
   directory of this project. E.g.
        C:\github\Utils2\Parsing\parsing-utils2\check-python33-manual
   b. Set the 'package/namespace for the generated code' to 'Gen.Grammar'.
   c. Finished with dialog: click OK.
4. Right click on the .g4 file in the IntelliJ editor again and select
   'Generate ANTLR Recognizer'. This will regenerate the Java source for the
   grammar into the 'Grammar/Gen' directory again.
??????????????????????

     
TODOs (maybe)
-------------
* Should really have the Python 2.7 and Python 3.3 grammars set up as modules
  of some kind that are used by the 'main checker code'!
* Java details on how to organize some of this not entirely clear to me.
    * E.g. better to use to Maven or Gradle organization.
* Java code in general needs a bit of a tidy up, but functional and serves
  its purpose for now. :-)

