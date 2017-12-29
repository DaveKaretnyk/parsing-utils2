// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.ArrayList;
import java.util.List;

/** Recursive listing of files in a directory. */
final class FileListing {

    /** Construct the recursive list of .py(w) files starting from the supplied dir as root.
     * @param dirRoot Dir to be processed.
     * @return The found .py files (full names) as list of strings.
     * @throws IOException IO exceptions might be thrown.
     */
    static List<String> buildList(String dirRoot) throws IOException {
        fileList = new ArrayList<>();
        ProcessFile fileProcessor = new ProcessFile();
        Files.walkFileTree(Paths.get(dirRoot), fileProcessor);

        return fileList;
    }

    /** Construct the recursive list of .py(w) files starting from the supplied dir as root.
     * @param dirRoot Dir to be processed.
     * @param ignoreSpecialDirs Files with 'test' or 'tests' will be ignored and any files with
     *                          'lib2to3' in their path will be ignored.
     * @return The found .py files (full names) as list of strings.
     * @throws IOException IO exceptions might be thrown.
     */
    static List<String> buildList(String dirRoot, boolean ignoreSpecialDirs) throws IOException {
        fileList = new ArrayList<>();
        ProcessFile fileProcessor = new ProcessFile();
        fileProcessor.ignoreSpecialDirs = ignoreSpecialDirs;
        Files.walkFileTree(Paths.get(dirRoot), fileProcessor);

        return fileList;
    }

    private static List<String> fileList = null;

    private static final class ProcessFile extends SimpleFileVisitor<Path> {
        boolean ignoreSpecialDirs = false;

        @Override
        public FileVisitResult visitFile(Path aFile,
                                         BasicFileAttributes aAttrs) throws IOException {
            // System.out.println("Processing file: " + aFile);
            String fileName = aFile.getFileName().toString();
            // System.out.println("Processing file: " + aFile.toString());
            // System.out.println("    parent path: " + aFile.getParent().endsWith("test"));
            // System.out.println("    parent path: " + aFile.getParent().endsWith("tests"));

            if (ignoreSpecialDirs) {
                if (aFile.getParent().endsWith("test") || aFile.getParent().endsWith("tests"))
                    return FileVisitResult.CONTINUE;
                if (aFile.getParent().toString().contains("lib2to3"))
                    return FileVisitResult.CONTINUE;
            }

            // Pick up .py, .pyw files, but binary extensions, byte code, or Cython input.
            // Excluding wheel files is a hack for processing the Standard Library sources which
            // contain a wheel file (e.g. pip-9.0.1-py2.py3-none-any.whl).
            if ((fileName.contains(".pyd")) || (fileName.contains(".pyc")) ||
                (fileName.contains(".pyx")) || (fileName.contains(".whl")))
                return FileVisitResult.CONTINUE;

            if (fileName.indexOf(".py") > 0)
                fileList.add(aFile.toString());

            return FileVisitResult.CONTINUE;
        }

        @Override
        public FileVisitResult preVisitDirectory(
                Path aDir, BasicFileAttributes aAttrs) throws IOException {
            // System.out.println("Processing directory: " + aDir);
            return FileVisitResult.CONTINUE;
        }
    }
}
