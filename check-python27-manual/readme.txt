Grammar checker for Python modules
**********************************
Check the grammar of the specified Python modules (files).

Purpose
-------
* Main features:
    * Client can specify either a single module (.py file) or list of modules
      (directory).
	* JUnit tests for a few miscellaneous files and for a snapshot of the
	  2.7.13 standard library sources.
	* Handle UTF-8 BOM marker in files - that tripped me up for a while.
* Shows how to setup and consume lexical and grammatical errors from the
  ANTLR framework.

Status
------
Working OK but grammar needs some attention - few spots to be looked into (see
TODOs listed in 'check-python27' project).

Grammar
-------
The grammar was developed by taking the Python 3.3 grammar from Bart Kiers:
	https://github.com/bkiers/python3-parser
Then diffing the official 2.7 grammar specification against the 3.3
specification to figure out what changes were needed.

Setup
-----
Manual setup within IntelliJ IDEA using the ANTLR plugin to configure how
grammar files are generated. Not the best organization, but useful as a
starting point to understand what is going on.

See also directory 'check-python33-manual' - same project organization but
uses Python 3.3 grammar from Bart Kiers.

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
See TODOs in readme.txt of project 'check-python27' - that is the project that
is more actively worked on.
