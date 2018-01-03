Generate UTC for a Python module
--------------------------------
Generate Unit Test Code for the specified Python module (file).

Main features:
    + ignores private free methods or private class methods (i.e. if name begins with '_').
    + All generated UTC is written to one fie.
    + UTC is output in the same order that it appears in the file being analyzed.


TODOs
-----
* Understand details of Python3.X grammar.
* Implement Python 2.7.X grammar.

* split UI code in separate folder? package?
* rename project: Java style.
* how to deploy?

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
