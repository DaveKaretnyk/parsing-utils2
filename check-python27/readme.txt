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
TODOs below).

Grammar
-------	  
The grammar was developed by taking the Python 3.3 grammar from Bart Kiers:
	https://github.com/bkiers/python3-parser
Then diffing the official 2.7 grammar specification against the 3.3
specification to figure out what changes were needed.

Setup
-----
Project setup is done via Maven pom.xml (compared to tha 'manual' IntelliJ
setup of project 'check-python27-manual'. This is a more sensible way to
organize things! :-)

A few aspects worthy of note
* The ANTLR Maven support is copied from:
    https://github.com/bkiers/python3-parser
* Number or additions made to pom.xml to support JUnit 5 from both Maven and
  IntelliJ IDED. Probably a bit more than strictly required, the pom.xml
  content was copied (then minor a few modifications) from:
    https://github.com/junit-team/junit5-samples/tree/master/junit5-maven-consumer
* The ANTLR plugin can probably still be used... But no real benefit and less
  confusing to just stick the the ANTLR Maven plugin that this project uses.
* Similarly, the project can be built from the IntelliJ 'Build' menu but that
  of course relies on the grammar being first translated to Java source. So
  again less confusing to just stick to Maven.
* Careful when running the ANTLR test rig. For example to display the parse
  tree graphically the following arguments are required (all one line):
        me.dave_karetnyk.utils.grammar.python27.Python27
        file_input -gui samples/source_with_errors/multiple_errors.py
  Note that the specification of the grammar file! It is case sensitive, so
  'python27' for the path and 'Python27' for the grammar file.
* The project dependencies: Java 1.8; JUnit 5; Apache Common IO 2.54; and of
  course ANTLR 4.7.1 are setup via the pom.xml.


TODOs (maybe)
-------------
* Some errors when processing the standard library sources. From an initial
  look they are mostly related to the print stmt? And also the warn stmt?
* Should really have the Python 2.7 and Python 3.3 grammars set up as modules
  of some kind that are used by the 'main checker code'!
* Some Maven details not entirely clear to me yet.
* Java code in general needs a bit of a tidy up, but functional and serves
  its purpose for now. :-)
* Related to previous comment - processing could be made more efficient (some
  obvious things to try).
* Check how Unicode should be handled for 2.7.X.
* Handle Encoding declarations properly?
* Check embedded Python code in the grammar in more detail.
* efficiency?
    * explicitly use SLL(*) grammar then LL(*) only if require?
    * don't keep recreating the grammar classes, e.g. not a new parser for
      every module!?
    * File IO operations are not done very sensibly ;-)
* split UI code in separate folder? package?
* sensible logging...
* get rid of ugly if (stdout)... code in CheckGrammar.execute().


Done
----
* Initial basic working version.
* catch grammar errors properly and record.
* JUnit test code.
* Efficiency?
    * Use setBuildParseTree(false)? Quick test - makes almost no difference.
* Archive copy of 2.7 standard library, e.g. for future testing.
* Understand details of Python27.g4 grammar.
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
* Java details on how to organize some of this not entirely clear to me.
    * E.g. better to use to Maven or Gradle organization.
