// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
package me.dave_karetnyk.utils.grammar.python27;

import java.io.File;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;


/** Analyze Python files (modules) according to the Python3.g4 grammar. */
public class CheckGrammar {
    /** Construct instance of class.
     * @param fileList List of files to check, client responsibility to supply good list.
     */
    private CheckGrammar(List<String> fileList) {
        listener = new Python27BaseListener();
        moduleList = fileList;
    }

    // list of .py files (modules) to be processed
    private List<String> moduleList = null;
    // Use the default generated listener, only the parsing will be of interest.
    private Python27BaseListener listener = null;

    /** Analyze the list of modules using the Python3.g4 grammar.
     * @return boolean True if parsed ok, else false.
     * @throws Exception Underlying exception from parser possible.
     */
    private void execute() throws Exception {
        int fileCounter = 0;
        boolean result = false;
        System.out.format(">>>>>>>>>  Will process %s modules\r\n", moduleList.size());
        LocalDateTime startTime = LocalDateTime.now();
        System.out.println("Time: " + startTime);
        for (String moduleName : moduleList) {
            System.out.println("Parsing: " + moduleName);
            result = processModule(moduleName);
            fileCounter++;
        }
        System.out.format(">>>>  processed %s modules\r\n", fileCounter);
        System.out.format("     >>>>  found %s errors\r\n", GrammarErrorListener.getNumErrors());
        LocalDateTime endTime = LocalDateTime.now();
        System.out.println("Time: " + endTime);
        return;
    }

    private boolean processModule(String moduleName) throws Exception {
        CharStream input = CharStreams.fromFileName(moduleName);
        Python27Lexer lexer = new Python27Lexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        Python27Parser parser = new Python27Parser(tokens);

        parser.setBuildParseTree(true);  // don't need parse tree -> set to false
        parser.removeErrorListeners(); // remove default ConsoleErrorListener
        GrammarErrorListener errorListener = new GrammarErrorListener();
        parser.addErrorListener(errorListener);
        ParseTree tree = parser.file_input();

        ParseTreeWalker walker = new ParseTreeWalker();
        walker.walk(listener, tree);

        return true;
    }

    /** Entry point for manually testing/running the CheckGrammar class.
     * @param args Name of file or directory to analyze.
     * @throws Exception Parser problems, input file problems, output file problems.
     */
    public static void main(String[] args) throws Exception {
        if (args.length == 0)
            throw new IllegalArgumentException("no file/dir supplied");

        List<String> fileList = new ArrayList<>();

        File fileOrDir = new File(args[0]);
        if (fileOrDir.isDirectory()) {
            fileList = FileListing.buildList(args[0]);
        }
        else {
            fileList.add(args[0]);
        }

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        checkGrammar.execute();
    }
}
