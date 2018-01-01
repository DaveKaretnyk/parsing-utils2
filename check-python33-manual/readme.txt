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

Code has same structure as the checker that was developed for Python 2.7.
This was done to give a reference point since the ANTLR 3.3 grammar is what
the 2.7 grammar was originally developed from. See directory 'check-python27-manual'.

Manual setup:
1. Assuming the ANTLR IntelliJ IDEA plugin in installed.
2. Create an IntelliJ project (type just 'plain Java') for the sources of this
   directory.
3. The project requires the following dependencies. So these need setup under
   Project Settings->Modules->Dependencies:
        Java 1.8; JUnit 5.0; Apache Common IO 2.54; ANTLR 4.7.1.
   So these need to be available from somewhere on your system.
   a. And under Project Settings->Modules-Source select the project root as a
      source directory and the 'Test' directory as a test directory.
4. Bring up the 'Configure ANTLR...' dialog (right click on the .g4 file in
   the IntelliJ editor.
   a. Set the 'Output directory to where all output is generated' to the root
      directory of this project. E.g.
        C:\github\Utils2\Parsing\parsing-utils2\check-python33-manual
   b. Set the 'package/namespace for the generated code' to 'Grammar.Gen'.
   c. Finished with dialog: click OK.
5. Right click on the .g4 file in the IntelliJ editor again and select
   'Generate ANTLR Recognizer'. This will re-generate the Java source for the
   grammar into the 'Grammar/Gen' directory again.
6. Build the Java source (Build->Build Project).
7. Any of the tests in CheckGrammarTest or AntlrSyntaxErrorTest can now be
   run.
8. To run the ANTLR test rig (see ANTLR documentation), e.g.
   a. Under 'Edit Configurations...' add an 'Application' configuration with
      settings:
        main class:     org.antlr.v4.gui.TestRig
        program args:   Grammar.Gen.Python27 file_input -gui samples/temp.py
      Of course TestRig supports other possibilities (see docs).
9. To run the main CheckGrammar class, e.g.
   a. Under 'Edit Configurations...' add an 'Application' configuration with
      settings:
        main class:     CheckGrammar
        program args:   samples/miscellaneous errors.log
      The first argument can be either a specific .py file or a directory
      containing .py files. The second argument is where the errors will be
      logged.

     
TODOs (maybe)
-------------
* One known grammar issue? 2 failures in .../Lib/http/client.py - something
  to do with string literal passed to re.compile(...)
        _is_legal_header_name = re.compile(rb'[^:\s][^:\r\n]*\Z').match
        _is_illegal_header_value = re.compile(rb'\n(?![ \t])|\r(?![ \t\n])').search
  Original grammar @ https://docs.python.org/3.3/reference/lexical_analysis.html.
  This piece of code not present in the 3.3.X sources used by Bart Kiers at
  the time so problem not seen there. But similar problem seen elsewhere - see
  repo, file Python3ParserTest.java, method 'not_sure_whats_wrong':
        https://github.com/bkiers/python3-parser
* Should really have the Python 2.7 and Python 3.3 grammars set up as modules
  of some kind that are used by the 'main checker code'!
* Java details on how to organize some of this not entirely clear to me.
    * E.g. better to use to Maven or Gradle organization.
* Java code in general needs a bit of a tidy up, but functional and serves
  its purpose for now. :-)
* Related to previous comment - processing could be made more efficient (some
  obvious things to try).
* See TODOs in readme.txt check-python27-manual project, some might apply here
  also.
