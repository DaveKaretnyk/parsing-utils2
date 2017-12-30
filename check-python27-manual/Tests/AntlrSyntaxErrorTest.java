// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class AntlrSyntaxErrorTest {
    static private AntlrSyntaxError antlrSyntaxError;

    @BeforeAll
    static void SetupBeforeAllTests() {
        List<String> ruleStack = new ArrayList<>();
        ruleStack.add("first rule on stack");
        ruleStack.add("second rule on stack");
        ruleStack.add("third rule on stack");

        antlrSyntaxError = new AntlrSyntaxError(".../path/to/some/file.py",
                                                 new Object(),
                                                21,
                                                45,
                                                "some message",
                                                 ruleStack);
    }

    @Test
    void getOffendingSymbol() {
        assertNotNull(antlrSyntaxError.getOffendingSymbol());
        assertEquals(AntlrSyntaxError.class, antlrSyntaxError.getClass());
    }

    @Test
    void getLine() {
        assertEquals(21, antlrSyntaxError.getLine());
    }

    @Test
    void getCharPositionInLine() {
        assertEquals(45,
                      antlrSyntaxError.getCharPositionInLine());
    }

    @Test
    void getMsg() {
        assertEquals("some message", antlrSyntaxError.getMsg());
    }

    @Test
    void getRuleStack() {
        List<String> expectedRuleStack = new ArrayList<>();
        expectedRuleStack.add("first rule on stack");
        expectedRuleStack.add("second rule on stack");
        expectedRuleStack.add("third rule on stack");

        assertTrue(expectedRuleStack.equals(antlrSyntaxError.getRuleStack()));
    }

    @Test
    void getFileName() {
        assertEquals(".../path/to/some/file.py",
                      antlrSyntaxError.getFileName());
    }

}