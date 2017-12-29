// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
import java.io.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.io.input.BOMInputStream;

import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;

import Grammar.Gen.Python33BaseListener;
import Grammar.Gen.Python33Lexer;
import Grammar.Gen.Python33Parser;


/** Analyze Python files (modules) according to the Python33.g4 grammar. */
public class CheckGrammar {
    /** Construct instance of class.
     * @param fileList List of files to check, client responsibility to supply a good list.
     */
    CheckGrammar(List<String> fileList) {
        this(fileList, false);
    }

    /** Construct instance of class.
     * @param fileList List of files to check, client responsibility to a supply good list.
     * @param stdout Trace information to stdout during processing.
     */
    CheckGrammar(List<String> fileList, boolean stdout) {
        listener = new Python33BaseListener();
        moduleList = fileList;
        this.stdout = stdout;
    }

    // list of .py files (modules) to be processed
    private List<String> moduleList;
    // Listener that consumes the syntax errors from the grammar.
    private GrammarErrorListener errorListener = null;
    // Use the default generated listener, only the parsing will be of interest.
    private Python33BaseListener listener;
    // Information to stdout?
    private boolean stdout;

    /** Analyze the list of modules using the Python33.g4 grammar.
     * @param logFileName Name of log file.
     * @return int Number of detected errors.
     * @throws Exception Underlying exception from parser possible.
     */
    int execute(String logFileName) throws Exception {
        execute();

        try {
            FileWriter fileWriter = new FileWriter(logFileName);

            fileWriter.write(String.format("%d processed module/s\n", moduleList.size()));
            fileWriter.write(String.format("%d errors found\n\n", errorListener.getNumErrors()));

            for (AntlrSyntaxError error:
                 errorListener.getAntlrSyntaxErrorList()) {
                fileWriter.write(
                        String.format("\tfilename:              %s\n", error.getFileName()));
                fileWriter.write(
                        String.format("\tline, char position    %d,%d\n",
                                      error.getLine(), error.getCharPositionInLine()));
                fileWriter.write(
                        String.format("\tmessage:               %s\n", error.getMsg()));
                fileWriter.write(
                        String.format("\trule stack:            %s\n\n", error.getRuleStack()));
            }

            fileWriter.close();

        } catch (IOException e) {
            System.out.format("Error writing to file %s, exception: %s\n",
                              logFileName, e.getMessage());
        }

        return errorListener.getNumErrors();
    }

    /** Analyze the list of modules using the Python33.g4 grammar.
     * @return int Number of detected errors.
     * @throws Exception Underlying exception from parser possible.
     */
    int execute() throws Exception {
        int fileCounter = 0;
        if (stdout) {
            System.out.format(">>>>>>>>>  Will process %d module/s\n", moduleList.size());
        }
        LocalDateTime startTime = LocalDateTime.now();
        if (stdout) {
            System.out.format("Time: %s\n\n", startTime);
        }

        errorListener = new GrammarErrorListener();

        for (String moduleName : moduleList) {
            int numErrors = processModule(moduleName, errorListener);
            fileCounter++;
            if (stdout) {
                System.out.format("Parsed  %s\t\t\t\t\t%d errors\n\b", moduleName, numErrors);
            }
        }

        LocalDateTime endTime = LocalDateTime.now();
        if (stdout) {
            System.out.format(">>>>  processed %d module/s\n", fileCounter);
            System.out.format(">>>>  found %d errors\n", errorListener.getNumErrors());
            System.out.println("Time: " + endTime);
        }

        return errorListener.getNumErrors();
    }

    /** Return current list of syntax errors.
     *
     * Null returned if parser has not been executed yet.
     * @return List<AntlrSyntaxError>
     */
    List<AntlrSyntaxError> getAntlrSyntaxErrorList() {
        return errorListener.getAntlrSyntaxErrorList();
    }

    /**
     * Reset the number of errors to 0, and the associated error list to null.
     */
    void resetErrors() {
        if (errorListener != null) errorListener.resetErrors();
    }

    /** Entry point for manually testing/running the CheckGrammar class.
     * @param args 1st arg is module/package name to analyze, 2nd arg is log file name.
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

        CheckGrammar checkGrammar = new CheckGrammar(fileList, true);

        int totalNumErrors;
        if (args.length > 1)
            totalNumErrors = checkGrammar.execute(args[1]);
        else
            totalNumErrors = checkGrammar.execute();

        System.out.format("\n\n*********  overall errors %d *********\n", totalNumErrors);
    }

    // -------------------------------------------------------------------------------------------
    // private helpers
    private int processModule(String moduleName, GrammarErrorListener errorListener)
            throws Exception {
        InputStream inputStream = new FileInputStream(moduleName);
        // Wrap the supplied stream and exclude any UTF-8 BOM.
        BOMInputStream bomStream = new BOMInputStream(inputStream);

        CharStream input = CharStreams.fromStream(bomStream);
        Python33Lexer lexer = new Python33Lexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        Python33Parser parser = new Python33Parser(tokens);

        if (stdout) {
            System.out.format("build parse tree? true\n");
        }
        parser.setBuildParseTree(true);  // don't need parse tree -> set to false

        // Remove default ConsoleErrorListener from both lexer and parser.
        lexer.removeErrorListeners();
        parser.removeErrorListeners();

        errorListener.setFileName(moduleName);
        errorListener.setStdout(stdout);

        // Add error listeners specific for this application.
        lexer.addErrorListener(errorListener);
        parser.addErrorListener(errorListener);

        int totalErrorsBefore = errorListener.getNumErrors();
        ParseTree tree = parser.file_input();

        ParseTreeWalker walker = new ParseTreeWalker();
        walker.walk(listener, tree);

        return errorListener.getNumErrors() - totalErrorsBefore;
    }

}
