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
    void test_integer_suffix() throws Exception {
        String module = "samples/miscellaneous/test_integer_suffix.py";
        List<String> fileList = new ArrayList<>();
        fileList.add(module);

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();

        if (printDiagnostics)
            System.out.format("\t%d errors\t\tfile:\t%s\n", errors, module);
        assertEquals(16, errors);
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
    void miscellaneous_directory_Test() throws Exception {
        String directory = "samples/miscellaneous";
        List<String> fileList = FileListing.buildList(directory);

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();

        if (printDiagnostics)
            System.out.format("\t%d errors\t\tdirectory:\t%s\n", errors, directory);
        assertEquals(16, errors);
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
    void standard_library_Test() throws Exception {
        // Process a copy of the 3.3.7 standard library sources.
        // Don't process files in 'test' or 'tests' directories or files with 'lib2to3' in their
        // path -> they often contain code that is not grammatically correct. This is more
        // practical than manually going through all files and selectively disabling as this would
        // need done each time the lib gets updated.
        String directory = "samples/standard_library_337/";
        List<String> fileList = FileListing.buildList(directory, true);

        CheckGrammar checkGrammar = new CheckGrammar(fileList, true);
        int errors = checkGrammar.execute("standard_library_errors.log");

        // See log file - 2 failures in .../Lib/http/client.py - something to do with string
        // literal passed to re.compile(...)
        //      _is_legal_header_name = re.compile(rb'[^:\s][^:\r\n]*\Z').match
        //      _is_illegal_header_value = re.compile(rb'\n(?![ \t])|\r(?![ \t\n])').search
        // Original grammar @ https://docs.python.org/3.3/reference/lexical_analysis.html.
        // This piece of code not present in the 3.3.X sources used by Bart Kiers at the time so
        // problem not seen there. But similar problem seen elsewhere - see repo, file
        // Python3ParserTest.java, method 'not_sure_whats_wrong':
        //      https://github.com/bkiers/python3-parser
        if (printDiagnostics)
            System.out.format("\t%d errors\t\tdirectory:\t%s\n", errors, directory);
        assertEquals(2, errors);
    }

    @Test
    void utf_8_bom_files_Test() throws Exception {
        String directory = "samples/utf_8_bom";
        List<String> fileList = FileListing.buildList(directory, false);

        CheckGrammar checkGrammar = new CheckGrammar(fileList);
        int errors = checkGrammar.execute();
        List<AntlrSyntaxError> errorList = checkGrammar.getAntlrSyntaxErrorList();

        if (printDiagnostics) {
            System.out.format("\t%d errors\t\tdirectory:\t%s\n", errors, directory);
        }
        assertEquals(0, errors);
    }

    // -------------------------------------------------------------------------------------------
    // private helpers

}
