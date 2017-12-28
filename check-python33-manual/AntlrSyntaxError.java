import java.util.List;

/**
 * POD encapsulation of ANTLR syntax error.
 *
 * Plain old data object that encapsulates the useful information of an ANTLR
 * syntax error.
 */
class AntlrSyntaxError {
    private String fileName;
    private Object offendingSymbol;
    private int line;
    private int charPositionInLine;
    private String msg;
    private List<String> ruleStack;

    AntlrSyntaxError(String fileName, Object offendingSymbol, int line, int charPositionInLine,
                     String msg, List<String> ruleStack) {
        this.fileName = fileName;
        this.offendingSymbol = offendingSymbol;
        this.line = line;
        this.charPositionInLine = charPositionInLine;
        this.msg = msg;
        this.ruleStack = ruleStack;

    }

    /** Return the problem symbol as a Object.
     * @return Object
     */
    Object getOffendingSymbol() {
        return offendingSymbol;
    }

    /** Get the line number where the problem occurs (numbering from 1).
     * @return int
     */
    int getLine() {
        return line;
    }

    /** Get the char position where the problem occurs (numbering from 0).
     * @return int
     */
    int getCharPositionInLine() {
        return charPositionInLine;
    }

    /** Get the error message supplied by ANTLR.
     * @return String
     */
    String getMsg() {
        return msg;
    }

    /** Get the parser rule stack defining the error (last element is the
     * top of stack).
     * @return List<String>
     */
    List<String> getRuleStack() {
        return ruleStack;
    }

    /** Name of the file where the problem was detected.
     * @return String
     */
    String getFileName() {
        return fileName;
    }
}
