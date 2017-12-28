Grammar checker for Python modules
----------------------------------
Check the grammar of the specified Python modules (files).

Manual setup within IntelliJ IDEA using the ANTLR plugin to configure how
grammar files are generated. Not the best organization, but useful as a
starting point to understand what is going on.

Main features:
    + Client can specify either a single module (.py file) or list of modules
     (directory).


Copy of the main checker that was developed for Python 2.7. This is to provide
a reference point since the ANTLR 3.3 grammar is the what the 2.7 grammar was
developed from.

     
TODOs
-----
* Should really have the Python 2.7 and Python 3.3 grammars set up as modules
  of some kind that are used by the 'main checker code'!
* Java details on how to organize this best not currently clear to me.
    * Convert to Maven or Gradle organization.
* Java code in general needs a bit of a tidy up, but functional and serves
  its purpose for now.
