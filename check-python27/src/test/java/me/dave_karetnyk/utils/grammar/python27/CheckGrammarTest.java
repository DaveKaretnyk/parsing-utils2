// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
package me.dave_karetnyk.utils.grammar.python27;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@SuppressWarnings("Duplicates")
class CheckGrammarTest {
    private boolean printDiagnostics = true;

    @Test
    void empty__init__Test() throws Exception {
        String module = "samples/miscellaneous/__init__.py";
        List<String> fileList = new ArrayList<>();
        fileList.add(module);

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();

        if (printDiagnostics)
            System.out.format("\t%d errors\t\tfile:\t%s\n", errors, module);
        assertEquals(0, errors);
    }

    @Test
    void sample1_Test() throws Exception {
        String module = "samples/miscellaneous/sample1.py";
        List<String> fileList = new ArrayList<>();
        fileList.add(module);

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();

        if (printDiagnostics)
            System.out.format("\t%d errors\t\tfile:\t%s\n", errors, module);
        assertEquals(0, errors);
    }

    @Test
    void try_except_Test() throws Exception {
        String module = "samples/miscellaneous/test_exception.py";
        List<String> fileList = new ArrayList<>();
        fileList.add(module);

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();

        if (printDiagnostics)
            System.out.format("\t%d errors\t\tfile:\t%s\n", errors, module);
        assertEquals(0, errors);
    }

    @Test
    void integer_suffix_Test() throws Exception {
        String module = "samples/miscellaneous/test_integer_suffix.py";
        List<String> fileList = new ArrayList<>();
        fileList.add(module);

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();

        if (printDiagnostics)
            System.out.format("\t%d errors\t\tfile:\t%s\n", errors, module);
        assertEquals(0, errors);
    }

    @Test
    void test_manual_sample1_Test() throws Exception {
        String module = "samples/miscellaneous/test_manual_sample1.py";
        List<String> fileList = new ArrayList<>();
        fileList.add(module);

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();

        if (printDiagnostics)
            System.out.format("\t%d errors\t\tfile:\t%s\n", errors, module);
        assertEquals(0, errors);
    }

    @Test
    void octal_parameter_Test() throws Exception {
        String module = "samples/miscellaneous/test_octal_as_named_para.py";
        List<String> fileList = new ArrayList<>();
        fileList.add(module);

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();

        if (printDiagnostics)
            System.out.format("\t%d errors\t\tfile:\t%s\n", errors, module);
        assertEquals(0, errors);
    }

    @Test
    void test_with_form_feed_char() throws Exception {
        String module = "samples/miscellaneous/with_form_feed_char.py";
        List<String> fileList = new ArrayList<>();
        fileList.add(module);

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();

        if (printDiagnostics)
            System.out.format("\t%d errors\t\tfile:\t%s\n", errors, module);
        assertEquals(0, errors);
    }

    @Test
    void print_statement_Test() throws Exception {
        String module = "samples/miscellaneous/test_print.py";
        List<String> fileList = new ArrayList<>();
        fileList.add(module);

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();

        if (printDiagnostics)
            System.out.format("\t%d errors\t\tfile:\t%s\n", errors, module);
        assertEquals(0, errors);
    }

    @Test
    void miscellaneous_directory_Test() throws Exception {
        String directory = "samples/miscellaneous";
        List<String> fileList = FileListing.buildList(directory);

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();

        if (printDiagnostics)
            System.out.format("\t%d errors\t\tdirectory:\t%s\n", errors, directory);
        assertEquals(0, errors);
    }

    @Test
    void bad_files_directory_Test() throws Exception {
        String directory = "samples/bad_files";
        List<String> fileList = FileListing.buildList(directory);

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();

        if (printDiagnostics)
            System.out.format("\t%d errors\t\tdirectory:\t%s\n", errors, directory);
        assertEquals(0, errors);
    }

    @Test
    void utf_8_bom_files_Test() throws Exception {
        String directory = "samples/utf_8_bom";
        List<String> fileList = FileListing.buildList(directory);

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();
        List<AntlrSyntaxError> errorList = checkGrammar.getAntlrSyntaxErrorList();

        if (printDiagnostics) {
            System.out.format("\t%d errors\t\tdirectory:\t%s\n", errors, directory);
        }
        assertEquals(0, errors);
    }

    @Test
    // Not run automatically, only if explicitly selected.
    void standard_library_Test() throws Exception {
        // Process a copy of the 2.7.13 standard library sources.
        // Don't process files in 'test' or 'tests' directories or files with 'lib2to3' in their
        // path -> they often contain code that is not grammatically correct. This is more
        // practical than manually going through all files and selectively disabling as this would
        // need done each time the lib gets updated.
        String directory = "../samples/standard_library_27_13/";
        List<String> fileList = FileListing.buildList(directory, true);

        CheckGrammar checkGrammar = new CheckGrammar(fileList, true);
        int errors = checkGrammar.execute("standard_library_errors.log");

        // TODO???
        // Some issue to look into. Mainly some special handling for print stmt required? And
        // issue with deprecated warn stmt?
        if (printDiagnostics)
            System.out.format("\t%d errors\t\tdirectory:\t%s\n", errors, directory);
        assertEquals(48, errors);
    }

    // -------------------------------------------------------------------------------------------
    // Some simple tests of files with syntax errors.
    @Test
    void configuation_control_Test() throws Exception {
        String module = "samples/source_with_errors/no_nl_at_eof.py";
        List<String> fileList = new ArrayList<>();
        fileList.add(module);

        // CheckGrammar checkGrammar = new CheckGrammar(fileList, true);
        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();
        List<AntlrSyntaxError> errorList = checkGrammar.getAntlrSyntaxErrorList();

        assertEquals(1, errors);
        assertEquals(1, errorList.size());
        AntlrSyntaxError error = errorList.get(0);
        if (printDiagnostics) {
            System.out.format("error message:\t\t%s\n", error.getMsg());
            System.out.format("\tline:      %d\n", error.getLine());
            System.out.format("\tcharacter: %s\n", error.getCharPositionInLine());
        }
        assertEquals(14, error.getLine());
        assertEquals(40, error.getCharPositionInLine());
    }

    @Test
    void multiple_errors_Test() throws Exception {
        String module = "samples/source_with_errors/multiple_errors.py";
        List<String> fileList = new ArrayList<>();
        fileList.add(module);

        // CheckGrammar checkGrammar = new CheckGrammar(fileList, true);
        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();
        List<AntlrSyntaxError> errorList = checkGrammar.getAntlrSyntaxErrorList();

        assertEquals(2, errors);
        assertEquals(2, errorList.size());

        AntlrSyntaxError error1 = errorList.get(0);
        if (printDiagnostics) {
            System.out.format("error message:\t\t%s\n", error1.getMsg());
            System.out.format("\tline:      %d\n", error1.getLine());
            System.out.format("\tcharacter: %s\n", error1.getCharPositionInLine());
        }
        assertEquals(5, error1.getLine());
        assertEquals(8, error1.getCharPositionInLine());

        AntlrSyntaxError error2 = errorList.get(1);
        if (printDiagnostics) {
            System.out.format("error message:\t\t%s\n", error2.getMsg());
            System.out.format("\tline:      %d\n", error2.getLine());
            System.out.format("\tcharacter: %s\n", error2.getCharPositionInLine());
        }
        assertEquals(15, error2.getLine());
        assertEquals(34, error2.getCharPositionInLine());
    }

    @Test
    void all_error_source_files_Test() throws Exception {
        String directory = "samples/source_with_errors";
        List<String> fileList = FileListing.buildList(directory);

        CheckGrammar checkGrammar = new CheckGrammar(fileList, true);
        //  CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();
        List<AntlrSyntaxError> errorList = checkGrammar.getAntlrSyntaxErrorList();

        assertEquals(3, errors);
        assertEquals(3, errorList.size());

    }

    // -------------------------------------------------------------------------------------------
    // private helpers

}
