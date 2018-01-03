// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
package me.dave_karetnyk.utils.grammar.python27;

import java.io.File;
import java.util.*;

import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;


/** Generate Python UTC for the specified file (module) according to the Python27.g4 grammar. */
public class Utc {
    /** Construct instance of class.
     * @param inputFileName File to be processed.
     */
    Utc(String inputFileName) {
        listener = new FunctionListener();

        File f = new File(inputFileName);
        if (!f.exists()) {
            throw new IllegalArgumentException("file cannot be found: " + inputFileName);
        }
        listener.setInputModuleName(inputFileName);
    }

    private FunctionListener listener = null;

    /** Sub-class of grammar's base listener (just override the parts of interest). */
    public class FunctionListener extends Python27BaseListener {
        SymbolTable symbolTable = new SymbolTable();

        /** Track nesting of classes. */
        Stack<String> classStack = new Stack<>();
        /** Track nesting of functions. */
        Stack<String> functionStack = new Stack<>();

        /** The name of the Python file (module) to be analyzed.
         * @param inputFileName Input file.
         */
        void setInputModuleName(String inputFileName) {
            symbolTable.setInputModuleName(inputFileName);
        }

        public void enterFuncdef(Python27Parser.FuncdefContext ctx) {
            String name = ctx.NAME().getText();
            functionStack.push(name);

            // private functions, free or within class, can be skipped
            if (name.substring(0, 1).equals("_")) {
                System.out.println("    > enter func, ignore private: " + name);
                return;
            }
            // local/nested functions, free or within class, can be skipped
            if (functionStack.size() != 1) {
                System.out.println("    > enter func, ignore local/nested: " + name);
                return;
            }

            if (classStack.size() == 1){
                // member function of a 'top level' class
                symbolTable.classMap.get(classStack.peek()).add(name);
                System.out.println("    > enter class func, track it: " + name);
            }
            else if (classStack.size() == 0) {
                // no class -> free function
                symbolTable.freeFuncList.add(name);
                System.out.println("> enter free func, track it: " + name);
            }
            else {
                System.out.println("    > function in nested class, ignore it: "
                                   + classStack.peek());
            }
        }

        public void exitFuncdef(Python27Parser.FuncdefContext ctx) {
            String name = ctx.NAME().getText();
            System.out.println("< leave function" + name);
            functionStack.pop();
        }

        public void enterClassdef(Python27Parser.ClassdefContext ctx) {
            String name = ctx.NAME().getText();
            classStack.push(name);

            // private classes, any scope, can be skipped
            if (name.substring(0, 1).equals("_")) {
                System.out.println("    > enter class, ignore private: " + name);
                return;
            }
            // local/nested classes can be skipped, i.e. only 'top level' classes of interest
            if (classStack.size() > 1) {
                System.out.println("    > enter class, ignore local/nested: " + name);
                return;
            }

            // have a class potentially of interest
            symbolTable.classMap.put(name, new ArrayList<>());
            System.out.println("> enter class: " + name);
        }

        public void exitClassdef(Python27Parser.ClassdefContext ctx) {
            String name = ctx.NAME().getText();
            System.out.println("< leave class: " + name);
            classStack.pop();
        }
    }

    /** Analyze the current file (module) using the Python3.g4 grammar, returns data structure
     * from which the UTC can be created.
     * @return SymbolTable Data structure.
     * @throws Exception Underlying exception from parser possible.
     */
    SymbolTable generateSymbols() throws Exception {
        CharStream input = CharStreams.fromFileName(listener.symbolTable.inputFileName);
        Python27Lexer lexer = new Python27Lexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        Python27Parser parser = new Python27Parser(tokens);
        parser.setBuildParseTree(true);
        ParseTree tree = parser.file_input();

        ParseTreeWalker walker = new ParseTreeWalker();
        walker.walk(listener, tree);

        return listener.symbolTable;
    }

    /** Process symbol table passed as argument, return the UTC as a string.
     * @param symbolTable SymbolTable to generate the UTC from.
     * @return UTC as string.
     * @throws Exception Parser problems, output file problems.
     */
    String render(SymbolTable symbolTable) throws Exception {
        return UtcRender.execute(symbolTable);
    }

    /** Entry point for manually testing/running the Utc class.
     * @param args Name of file to analyze.
     * @throws Exception Parser problems, input file problems, output file problems.
     */
    public static void main(String[] args) throws Exception {
        if (args.length == 0)
            throw new IllegalArgumentException("name of file to analyze must be passed");

        Utc utc = new Utc(args[0]);
        SymbolTable symbolTable = utc.generateSymbols();

        System.out.println("---------------------------------------------------------------");
        System.out.println("Free functions");
        for (String funcName : symbolTable.freeFuncList) {
            System.out.println("\t" + funcName);
        }

        System.out.println("---------------------------------------------------------------");
        System.out.println("Class functions");
        for (String className: symbolTable.classMap.keySet()) {
            System.out.println("\t" + className);
            for (String funcName: symbolTable.classMap.get(className) ) {
                System.out.println("\t\t" + funcName);
            }
        }
        System.out.print("\r\n\r\n");

        System.out.println("---------------------------------------------------------------");
        System.out.println("UTC output");
        String result = utc.render(symbolTable);
        System.out.println(result);

        System.out.println("---------------------------------------------------------------");
        System.out.println("Copied to system clipboard");
        UiSystemClipboard.CopyTo(result);

    }
}
