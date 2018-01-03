// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
package me.dave_karetnyk.utils.grammar.python27;

import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/** Simple data class for retaining the required symbol information. */
class SymbolTable {
    /** The name of the input file/module to process. */
    String inputFileName = null;

    /** The name of the module to be processed. E.g. "sample1" for ".../blah/sample1.py" */
    String moduleName = null;

    /** Free functions, just a list of function names. */
    List<String> freeFuncList = new ArrayList<>();

    /** Map of class names; for each class name a list of zero/more member function names. */
    HashMap<String, ArrayList<String>> classMap = new HashMap<>();

    void setInputModuleName(String name) {
        inputFileName = name;

        String fileName = Paths.get(inputFileName).getFileName().toString();

        if (fileName.indexOf(".") > 0)
            moduleName = fileName.substring(0, fileName.lastIndexOf("."));
        else {
            throw new IllegalArgumentException("bad file name: " + inputFileName);
        }
    }
}
