// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
package me.dave_karetnyk.utils.grammar.python27;

import java.util.ArrayList;
import java.util.List;

import org.stringtemplate.v4.ST;

class UtcRender {
    private UtcRender() {} // restrict instantiation

    /** Process symbol table passed as argument, return the UTC as a string.
     * @param symbolTable SymbolTable to generate the UTC from.
     * @return UTC as string.
     * @throws Exception Parser problems, output file problems.
     */
    static String execute(SymbolTable symbolTable) throws Exception {
        String stGrammar = UtcTemplates.modulePreAmble + UtcTemplates.imports +
                UtcTemplates.freeFuncPreAmble + UtcTemplates.freeFunc;

        // Construct UTC based on the defined ST grammar.
        ST st = new ST(stGrammar);
        st.add("module", symbolTable.moduleName);
        st.add("classOrFuncList", getClassAndFunctionList(symbolTable));
        st.add("freeFuncsList", symbolTable.freeFuncList);
        String utc = st.render();

        // Helper will append the UTC for classes.
        utc = addClassUtcCode(utc, symbolTable);

        return utc;
    }

    private static String addClassUtcCode(String currentUtc, SymbolTable symbolTable) {
        String utc = currentUtc;
        for (String className : symbolTable.classMap.keySet()) {
            ST stClassGrammar = new ST(UtcTemplates.classDefPart);
            stClassGrammar.add("className", className);
            String newClass = stClassGrammar.render();
            utc += newClass;
            for (String classFunctionName : symbolTable.classMap.get(className)) {
                ST stFunctionGrammar = new ST(UtcTemplates.classFunctionPart);
                stFunctionGrammar.add("classFunctionName", classFunctionName);
                String newFunction = stFunctionGrammar.render();
                utc += newFunction;
            }
            utc += UtcTemplates.NL;
        }
        return utc;
    }

    private static List<String> getClassAndFunctionList(SymbolTable symbolTable) {
        List<String> targetList = new ArrayList<>(symbolTable.classMap.keySet());
        targetList.addAll(symbolTable.freeFuncList);
        return targetList;
    }
}
