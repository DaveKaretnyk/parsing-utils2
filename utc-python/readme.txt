Generate UTC stubs for a Python module
**************************************
Java program that generates Unit Test Code stubs for the specified Python
module (file).

Purpose
-------
* Main features:
    * Single argument to program - the name of the module (file) to be
      processed.
    * The output is written to standard output, but also to the clipboard to
      be then pasted wherever required.
    * The output consists of test method 'stubs', i.e. with no actual content
      but filled in with comments (TODOs) and assertions to then guide the
      adding the real test code.
    * Ignores private free methods or private class methods (i.e. if name
      begins with '_').
    * Ignores embedded/local classes and methods.
    * All generated UTC is written to one fie.
    * UTC is output in the same order that it appears in the file being
      analyzed.
* Shows how to setup and consume methods called by the ANTLR generated
  parse tree listener code, e.g. as a method is entered or exited.
* Basic use of StringTemplate (ST) library to output the required test code.
    http://www.stringtemplate.org/

Status
------
Working OK. But only very limited testing to date.

Grammar
-------
Python 2.7.13 grammar. Status and details - see 'check-python27' project in
this repository. The grammar contains embedded actions (written in Java) so
can only be used with Java as the target language.


TODOs
-----
* Does not pick up lexical or grammatical errors in the source file - just
  tries to continue.
* split UI code in separate folder? package?
* StringTemplate (ST) version - using the one that is bundled with ANTLR. Is
  more up to date version useful?
* StringTemplate (ST) use in general needs clean up.
* ST: imports: format multiline if > 100 chars.
* ST: imports: no separator for last import.
* ST: would like to generate class functions purely from ST.
* replace classStack and currentFunc structures by walking up the parse tree?

* sensible logging ;-)
* plugin for IntelliJ/PyCharm?

Done
----
* ignore nested/local free functions.
* JUnit UTC for the main analysis code.
* how to organize Antlr grammar and generated Java?
* handle class methods.
* ignore nested/local classes.
* add JavaDoc to main classes.
* handle properties: not needed.
* Use StringTemplate to generate output? Yes, bit of figuring out, but worthwhile.
* need to pass in module/file as parameter.
* UTC render of classes.
* UTC render for class functions.
* UTC render for imports.
* copy result to clipboard.
* test on various files!
    * small corpus of valid Python files: all from Mono, few from OptiMono.
    * Empty file: OK, get one test class with nothing in it.
    * Non Python files, e.g. garbage or Java code, ...
    * File with grammar error.
* process directory of files. Not for now, just handle single file.
* how to deploy? Via JAR.
