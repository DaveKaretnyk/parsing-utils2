// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
package me.dave_karetnyk.utils.grammar.python27;


class UtcTemplates {
    private UtcTemplates() {} // restrict instantiation

    static final String NL = "\r\n"; // Windows only newline

    static String modulePreAmble =
        "# Under MIT License, Copyright (c) 2017-18 Dave Karetnyk."                     +NL+
        "import unittest"                                                               +NL+
        ""                                                                              +NL;

    //TODO??? not quite, how to drop separator for last item...
    static String imports =
        "# TODO???"                                                                     +NL+
        "from enter.path.to.<module> import ("                                          +
        "<classOrFuncList:{f | <f>, "                                                   +"}>" +
        ")"                                                                             +NL+
        ""                                                                              +NL+
        ""                                                                              +NL;

    static String freeFuncPreAmble =
       "# TODO???"                                                                      +NL+
        "class Test_module_<module>(unittest.TestCase):"                                +NL+
        "    @classmethod"                                                              +NL+
        "    def setUpClass(cls):"                                                      +NL+
        "        pass"                                                                  +NL+
        ""                                                                              +NL+
        "    @classmethod"                                                              +NL+
        "    def tearDownClass(cls):"                                                   +NL+
        "        pass"                                                                  +NL+
        ""                                                                              +NL+
        "    def setUp(self):"                                                          +NL+
        "        self.diagnostics_print = False"                                        +NL+
        ""                                                                              +NL+
        "    def tearDown(self):"                                                       +NL+
        "        pass"                                                                  +NL+
        ""                                                                              +NL;

    // Template is mapped over by a list of free function names -> more tricky to clearly show, but
    // basically the following is generated, where <xxx> is the injected name:
    //     def test_<xxx>(self):
    //         self.assertTrue(False)
    //
    // Syntax of the iteration is:
    //     <items :{item | <item> }>
    // The :{ } construct can be read as '...for each item in items print item...'.
    static String freeFunc =
        "<freeFuncsList:{func | "                                                   + NL +
        "    # TODO???"                                                             + NL +
        "    def test_<func>(self):"                                                + NL +
        "        self.assertTrue(False)"                                            + NL +
        ""                                                                          + NL + "}>" +
        ""                                                                          + NL;

    static String classDefPart =
                    "# TODO???"                                                         +NL+
                    "class Test<className>(unittest.TestCase):"                         +NL+
                    "    @classmethod"                                                  +NL+
                    "    def setUpClass(cls):"                                          +NL+
                    "        pass"                                                      +NL+
                    ""                                                                  +NL+
                    "    @classmethod"                                                  +NL+
                    "    def tearDownClass(cls):"                                       +NL+
                    "        pass"                                                      +NL+
                    ""                                                                  +NL+
                    "    def setUp(self):"                                              +NL+
                    "        self.diagnostics_print = False"                            +NL+
                    ""                                                                  +NL+
                    "    def tearDown(self):"                                           +NL+
                    "        pass"                                                      +NL+
                    ""                                                                  +NL;

    static String classFunctionPart =
                "    # TODO???"                                                         +NL+
                "    def test_<classFunctionName>(self):"                               +NL+
                "        self.assertTrue(False)"                                        +NL+
                    ""                                                                  +NL;

    // See UtRender.java which shows client code doing the equivalent of the following...
    // Because I could not quite get this pure ST version below to work ;-) Can be done for sure.
    // Other aspect to consider though is which way is most readable?
    // Client to use what is below:
    //      // List<String> classNames = new ArrayList<>(symbolTable.classMap.keySet());
    //      // No need for above, use HashMap directly gives iterator of keys (i.e. class names).
    //      st.add("classMap", symbolTable.classMap);

    static String classDefinition =
            "<classMap.keys:{className | "                                              +
                    "class Test<className>(unittest.TestCase):"                         +NL+
                    "    @classmethod"                                                  +NL+
                    "    def setUpClass(cls)"                                           +NL+
                    "        pass"                                                      +NL+
                    ""                                                                  +NL+
                    "    @classmethod"                                                  +NL+
                    "    def tearDownClass(cls):"                                       +NL+
                    "        pass"                                                      +NL+
                    ""                                                                  +NL+
                    "    def setUp(self):"                                              +NL+
                    "        self.diagnostics_print = False"                            +NL+
                    ""                                                                  +NL+
                    "    def tearDown(self):"                                           +NL+
                    "        pass"                                                      +NL+
                    ""                                                                  +NL+
// TODO??? not quite - needs some work...
//                "    def test_<classMap.(className);separator=\"(self):"            +NL+
//                "        self.assertTrue(False)"                                    +NL+
//                "    "                                                              +NL+ "\">" +
                    ""                                                                  +NL+ "}>";
}
