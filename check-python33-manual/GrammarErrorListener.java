import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import org.antlr.v4.runtime.*;

/** Sub-class the default ANTLR Error Listener class. */
public class GrammarErrorListener extends BaseErrorListener {
    private String fileName = null;
    private int lexerErrors = 0;
    private int parserErrors = 0;
    private boolean stdout = false;

    private List<AntlrSyntaxError> antlrSyntaxErrorList = new ArrayList<>();

    @Override
    public void syntaxError(Recognizer<?, ?> recognizer,
                            Object offendingSymbol,
                            int line, int charPositionInLine,
                            String msg,
                            RecognitionException e) {
        List<String> ruleStack = null;
        if (recognizer instanceof Lexer) {
            lexerErrors++;
        }
        else {
            parserErrors++;
            ruleStack = ((Parser)recognizer).getRuleInvocationStack();
            Collections.reverse(ruleStack);
        }

        AntlrSyntaxError error = new AntlrSyntaxError(fileName, offendingSymbol, line,
                                                      charPositionInLine, msg, ruleStack);
        addToErrorList(error);

        if (stdout) {
            if (ruleStack != null) {
                System.out.print("RULE STACK:");
                System.out.println("\t\t\t\t" + ruleStack);
            }
            System.out.print("LINE, CHAR POS:");
            System.out.println("\t\t\t" + line + ":" + charPositionInLine);
            if (ruleStack != null) {
                System.out.print("OFFENDING SYMBOL:");
                System.out.println("\t\t" + offendingSymbol);
            }
            System.out.print("ERROR MESSAGE:");
            System.out.println("\t\t\t" + msg);
        }
    }

    /** Set the name of the file to be processed.
     *
     * @param fileName Sring
     */
    void setFileName(String fileName) {
        this.fileName = fileName;
    }

    /** Information to stdout during processing.
     *
     * @param stdout boolean
     */
    void setStdout(boolean stdout) {
        this.stdout = stdout;
    }

    /** Get number of syntax errors.
     *
     * @return int
     */
    int getNumErrors() {
        return lexerErrors + parserErrors;
    }

    /** Return current list of syntax errors (empty list if no errors).
     *
     * @return List<AntlrSyntaxError>
     */
    List<AntlrSyntaxError> getAntlrSyntaxErrorList() {
        return antlrSyntaxErrorList;
    }

    /** Reset the counter and list of syntax errors.
     *
     */
    void resetErrors() {
        lexerErrors = 0;
        parserErrors = 0;
        antlrSyntaxErrorList = null;
    }

    // -------------------------------------------------------------------------------------------
    // private helpers
    private void addToErrorList(AntlrSyntaxError error) {
        if (antlrSyntaxErrorList == null) {
            antlrSyntaxErrorList = new ArrayList<>();
        }
        antlrSyntaxErrorList.add(error);
    }
}
