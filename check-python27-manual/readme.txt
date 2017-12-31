Grammar checker for Python modules
----------------------------------
Check the grammar of the specified Python modules (files).

Main features:
    + Client can specify either a single module (.py file) or list of modules
     (directory).
	+ JUnit tests for a few miscellaneous files and for a snapshot of the
	  2.7.13 standard library sources.
	+ Handle UTF-8 BOM marker in files - that tripped me up for a while.

The grammar was derived by taking the Python 3.3 grammar from Bart Kiers:
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
        Java 1.8; JUnit 5.0; Apache Common IO 2.54; ANTLR 4.7.
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
* Some errors when processing the standard library sources. From an initial
  look they are mostly related to the print stmt? And also the warn stmt?
* Should really have the Python 2.7 and Python 3.3 grammars set up as modules
  of some kind that are used by the 'main checker code'!
* Java details on how to organize some of this not entirely clear to me.
    * E.g. better to use to Maven or Gradle organization.
* Java code in general needs a bit of a tidy up, but functional and serves
  its purpose for now. :-)
* Related to previous comment - processing could be made more efficient (some
  obvious things to try).
* Check how Unicode should be handled for 2.7.X.
* Handle Encoding declarations properly?
* Check embedded Python code in more detail.
* Understand details of Python27.g4 grammar.
* efficiency?
    * explicitly use SLL(*) grammar then LL(*) only if require?
    * don't keep recreating the grammar classes, e.g. not a new parser for
      every module!?
    * File IO operations are not done very sensibly ;-)
* split UI code in separate folder? package?
* sensible logging ;-)
* get rid of ugly if (stdout)... code in CheckGrammar.execute().


Done
----
* Initial basic working version.
* catch grammar errors properly and record.
* JUnit test code.
* Efficiency?
    * Use setBuildParseTree(false)? Quick test - makes almost no difference.
* Archive copy of 2.7 standard library, e.g. for future testing.
* Define sensible output format? Just simple log file and stdout for now?
* State / threading error: run all unit tests, sometimes test fails? Silly
  goof in my class FileListing.java! ;-)
    * 'bad_files_directory_Test' and 'miscellaneous_directory_Test' but this
      runs OK when run individually?
* File BOM marker signalling UTF-8 should be handled (see 'Lexical Analysis'
  rules of the 'Python Language Reference'.
    https://docs.python.org/2/reference/lexical_analysis.html
  Solved by using BOMInputStream from Apache Commons IO library, i.e. get rid
  of it before it even gets to the grammar.
* Lexer rules need formatting tidy up (in line with parser).
* Copyright? Leave MIT license from Kiers in place since that is where the
  implementation is mainly derived from.
* GrammarErrorListener - adjust so that lexer errors are handled too.
* how to deploy? Just pack into JAR (see notes elsewhere).
* plugin in for IntelliJ/PyCharm? Not really need, might set up Jenkins job.
