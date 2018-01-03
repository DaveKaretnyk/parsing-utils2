// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
package me.dave_karetnyk.utils.grammar.python27;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.nio.file.*;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MiscTest {
    private boolean printDiagnostics = true;

    @BeforeEach
    void setUp() {
    }

    @AfterEach
    void tearDown() {
    }

    @Test
    void moduleNameTest() {
        String testy = "input/sample1.py";
        if (printDiagnostics)
            System.out.println(testy);

        String fileName = Paths.get(testy).getFileName().toString();
        if (printDiagnostics)
            System.out.println(fileName);

        String moduleName = null;
        if (fileName.indexOf(".") > 0)
            moduleName = fileName.substring(0, fileName.lastIndexOf("."));
        else {
            throw new IllegalArgumentException("bad file name: " + testy);
        }

        if (printDiagnostics)
        System.out.println(moduleName);
        assertEquals("sample1", moduleName);
    }

    @Test
    void checkIfFileOrDir() throws IOException {
        File fileOrDir = new File("C:\\Windows");
        assertTrue(fileOrDir.isDirectory());

        fileOrDir = new File("C:\\pagefile.sys");
        assertTrue(fileOrDir.isFile());
    }

    @Test
    void filesInDirRecursive() throws IOException {
        String dirRoot = "C:\\github\\Parsers\\Antlr\\gen_python_utc";
        List<String> fileNameList = FileListing.buildList(dirRoot);

        if (printDiagnostics) {
            for (String fileName : fileNameList) {
                System.out.println(fileName);
            }
        }
    }
}

