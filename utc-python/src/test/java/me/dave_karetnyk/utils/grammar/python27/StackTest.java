// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
package me.dave_karetnyk.utils.grammar.python27;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Stack;

/**
 * Some simple tests while I get use to Java. ;-)
 */
class StackTest {
    @BeforeEach
    void setUp() {
    }

    @AfterEach
    void tearDown() {
    }

    @Test
    void basicTest() {
        Stack<String> stack = new Stack<>();
        assertTrue(stack.isEmpty());

        String first = "first";
        stack.push(first);
        assertFalse(stack.isEmpty());
        assertEquals(first, stack.peek());

        stack.push("second");
        assertFalse(stack.isEmpty());
        assertEquals("second", stack.peek());

        assertEquals("second", stack.pop());
        assertFalse(stack.isEmpty());

        assertEquals("first", stack.pop());
        assertTrue(stack.isEmpty());
    }
}
