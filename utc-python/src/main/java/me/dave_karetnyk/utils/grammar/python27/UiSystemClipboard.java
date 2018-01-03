// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
package me.dave_karetnyk.utils.grammar.python27;

import java.awt.*;
import java.awt.datatransfer.Clipboard;
import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.StringSelection;

/** Minial interop with the system clipboard.
 */
class UiSystemClipboard {
    private UiSystemClipboard() {} // restrict instantiation

    /** Copy the supplied string to the system clipboard.
     * @param string string to copy.
     */
    static void CopyTo(String string) {
        StringSelection selection = new StringSelection(string);
        Clipboard clipBoard = Toolkit.getDefaultToolkit().getSystemClipboard();
        clipBoard.setContents(selection, selection);
    }

    static String getFrom() throws Exception {
        String result = null;
        Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();

        DataFlavor dataFlavor = DataFlavor.stringFlavor;
        if (clipboard.isDataFlavorAvailable(dataFlavor))
        {
            Object text = clipboard.getData(dataFlavor);
            result = (String)text;
        }
        return result;
    }
}
