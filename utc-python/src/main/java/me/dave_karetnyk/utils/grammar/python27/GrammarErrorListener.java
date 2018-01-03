// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
package me.dave_karetnyk.utils.grammar.python27;

import org.antlr.v4.runtime.BaseErrorListener;
import org.antlr.v4.runtime.Parser;
import org.antlr.v4.runtime.RecognitionException;

import org.antlr.v4.runtime.Recognizer;

import java.util.Collections;
import java.util.List;

/** Sub-class the default ANTLR Error Listener class. */
public class GrammarErrorListener extends BaseErrorListener {
    private static int numErrors = 0;

    public static int getNumErrors() {
        return numErrors;
    }

    @Override
    public void syntaxError(Recognizer<?, ?> recognizer,
                            Object offendingSymbol,
                            int line, int charPositionInLine,
                            String msg,
                            RecognitionException e) {
        numErrors++;

        List<String> stack = ((Parser)recognizer).getRuleInvocationStack();
        Collections.reverse(stack);

//        System.err.println("rule stack: "+stack);
//        System.err.println("line "+line+":"+charPositionInLine+" at "+
//                offendingSymbol+": "+msg);

        System.out.print("RULE STACK:");
        System.out.println("\t\t\t\t" + stack);
        System.out.print("LINE, CHAR POS:");
        System.out.println("\t\t\t" + line + ":" + charPositionInLine);
        System.out.print("OFFENDING SYMBOL:");
        System.out.println("\t\t" + offendingSymbol);
        System.out.print("ERROR MESSAGE:");
        System.out.println("\t\t\t" + msg);
        System.out.println();
    }
}
