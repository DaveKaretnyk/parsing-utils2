// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
package me.dave_karetnyk.utils.grammar.python27;

import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.ArrayList;
import java.util.List;

/** Recursive listing of files in a directory. */
final class FileListing {

    /** Construct the recursive list of .py files starting from the supplied dir as root.
     * @param dirRoot Dir to be processed.
     * @return The found .py files (full names) as list of strings.
     * @throws IOException IO exceptions might be thrown.
     */
    static List<String> buildList(String dirRoot) throws IOException {
        FileVisitor<Path> fileProcessor = new ProcessFile();
        Files.walkFileTree(Paths.get(dirRoot), fileProcessor);

        return fileList;
    }

    private static List<String> fileList = new ArrayList<>();

    private static final class ProcessFile extends SimpleFileVisitor<Path> {
        @Override
        public FileVisitResult visitFile(Path aFile,
                                         BasicFileAttributes aAttrs) throws IOException {
            // System.out.println("Processing file: " + aFile);

            String fileName = aFile.getFileName().toString();
            // pick up .py, .pyw files, but binary extensions, byte code, or Cython input
            if ((!fileName.contains(".pyd"))&& (!fileName.contains(".pyc"))&&
                (!fileName.contains(".pyx")))
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
