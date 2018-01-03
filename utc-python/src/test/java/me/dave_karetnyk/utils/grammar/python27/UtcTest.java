// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
package me.dave_karetnyk.utils.grammar.python27;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class UtcTest {
    private boolean printDiagnostics = true;

    @BeforeEach
    void setUp() {
    }

    @AfterEach
    void tearDown() {
    }

    @Test
    void generate_symbols_sample1_py() throws Exception {
        Utc utc = new Utc("samples/sample1.py");
        SymbolTable symbolTable = utc.generateSymbols();

        if (printDiagnostics) {
            System.out.printf("%s free functions detected:%n", symbolTable.freeFuncList.size());
            for (String entry : symbolTable.freeFuncList) {
                System.out.println("    " + entry);
            }
        }

        List<String> expectFreeFuncs = Arrays.asList(
                "free_func_1", "free_func_2", "free_func_3", "free_func_4"
        );
        assertEquals(expectFreeFuncs, symbolTable.freeFuncList);

        if (printDiagnostics) {
            System.out.printf("%s class/es with functions detected:%n",
                              symbolTable.classMap.size());
            for (String className: symbolTable.classMap.keySet()) {
                System.out.println("\t" + className);
                for (String funcName: symbolTable.classMap.get(className) ) {
                    System.out.println("\t\t" + funcName);
                }
            }
        }

        HashMap<String, ArrayList<String>> expectedClassFuncs = new HashMap<>();
        expectedClassFuncs.put("Silly1", new ArrayList<>());
        expectedClassFuncs.get("Silly1").add("class_func_get1");
        expectedClassFuncs.get("Silly1").add("class_func_set1");

        expectedClassFuncs.put("Silly2", new ArrayList<>());
        expectedClassFuncs.get("Silly2").add("class_func_get2");
        expectedClassFuncs.get("Silly2").add("class_func_set2");
        expectedClassFuncs.get("Silly2").add("class_func_another");
        expectedClassFuncs.get("Silly2").add("class_func_another2");

        expectedClassFuncs.put("Silly3", new ArrayList<>());
        expectedClassFuncs.get("Silly3").add("class_func_get1");
        expectedClassFuncs.get("Silly3").add("class_func_set1");

        assertEquals(expectedClassFuncs.size(), symbolTable.classMap.size());
        assertEquals(expectedClassFuncs.get("Silly1"), symbolTable.classMap.get("Silly1"));
        assertEquals(expectedClassFuncs.get("Silly2"), symbolTable.classMap.get("Silly2"));
        assertEquals(expectedClassFuncs.get("Silly3"), symbolTable.classMap.get("Silly3"));
    }

    @Test
    void render_utc_sample1() throws Exception {
        Utc utc = new Utc("samples/sample1.py");
        SymbolTable symbolTable = utc.generateSymbols();

        String result = utc.render(symbolTable);
        if (printDiagnostics)
            System.out.print("\r\n\r\n");
            System.out.println(result);
        assertNotEquals(0, result.length());

        UiSystemClipboard.CopyTo(result);
        String fromClipboard = UiSystemClipboard.getFrom();
        assertEquals(fromClipboard, result);
    }
}
