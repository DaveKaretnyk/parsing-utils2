// Under MIT License, Copyright (c) 2017-18 Dave Karetnyk
// Full terms: see "LICENSE' file in root directory of repository:
//      https://github.com/DaveKaretnyk/parsing-utils2
package me.dave_karetnyk.utils.grammar.python27;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

import org.stringtemplate.v4.*;


/** Simple model to drive the view */
class MyUser {
    public int id;                          // see below, direct access via u.id
    private String name;                    // cannot access this
    public MyUser(int id, String name) {
        this.id = id;
        this.name = name;
    }
    public boolean isManager() {            // access via u.manager
        return true;
    }
    public boolean hasParkingSpot() {       // access via u.parkingSpot
        return true;
    }
    public String getName() {               // access via u.name
        return name;
    }
    public String toString() {              // access via u
        return id + ":" + name;
    }
}


/**
 * Some simple tests while I get use to Java. ;-)
 */
class StringTemplateTest {
    private boolean printDiagnostics = true;

    @BeforeEach
    void setUp() {
    }

    @AfterEach
    void tearDown() {
    }

    @Test
    void helloWorldTest() {
        ST hello = new ST("Hello there <name>!");
        hello.add("name", "World");

        if (printDiagnostics)
            System.out.println(hello.render());
        assertEquals("Hello there World!", hello.render());
    }

    @Test
    void stGroupDirTest() {
        String dirName = "src/test/java/me/dave_karetnyk/utils/grammar/python27";
        STGroup group = new STGroupDir(dirName);
        ST st = group.getInstanceOf("decl");
        assertNotNull(st);
        st.add("type", "int");
        st.add("name", "x");
        st.add("value", 0);

        String result = st.render();
        if (printDiagnostics)
            System.out.println(result);
        assertEquals("int x = 0;", result);
    }

    @Test
    void stGroupFileTest() {
        String fileName = "src/test/java/me/dave_karetnyk/utils/grammar/python27/groupFile.stg";
        STGroup group = new STGroupFile(fileName);
        ST st = group.getInstanceOf("decl");
        assertNotNull(st);
        st.add("type", "int");
        st.add("name", "x");
        st.add("value", 0);

        String result = st.render();
        if (printDiagnostics)
            System.out.println(result);
        assertEquals("int x = 0;", result);
    }

    @Test
    void modelPropertiesTest() {
        // define the view
        ST st = new ST("<b>$u.id$</b>: $u.name$",
                       '$', '$');

        // simple model to drive some parts of the view
        MyUser myUser = new MyUser(999, "parrt");
        st.add("u", myUser);

        // output/render the view
        String result = st.render();
        if (printDiagnostics)
            System.out.println(result);
        assertEquals("<b>999</b>: parrt", result);
    }

    @Test
    void modelProperties2Test() {
        // define the view
        String temp =
                        "<b>$u.id$</b>: $u.name$\r\n" +
                        "\tmanager:\t\t$u.manager$\r\n" +
                        "\tparking spot:\t$u.parkingSpot$\r\n";
        ST st = new ST(temp,'$', '$');

        // simple model to drive some parts of the view
        MyUser myUser = new MyUser(999, "parrt");
        st.add("u", myUser);

        // output/render the view
        String result = st.render();
        if (printDiagnostics)
            System.out.println(result);
        String expected =
                "<b>999</b>: parrt\r\n" +
                        "\tmanager:\t\ttrue\r\n" +
                        "\tparking spot:\ttrue\r\n";

        assertEquals(expected, result);
    }

    @Test
    void stFormatTest() {
        int[] num = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18};
        String t = ST.format(30,
                             "int <%1>[] = { <%2; wrap, anchor, separator=\", \"> };",
                             "a", num);

        if (printDiagnostics)
            System.out.println(t);
    }

    @Test
    void stIterateJavaList() {
        List<String> teams = Arrays.asList(
                "Cats", "Birds", "Turtles", "Penguins"
        );

        ST s = new ST("<teams :{team | <team>; }>");
        s.add("teams", teams);
        System.out.println(s.render());
    }

    @Test
    void stMapVariableOverTemplate() {
        List<String> funcsList = Arrays.asList(
                "free_func_1", "free_func_2", "free_func_3", "free_func_4"
        );

        ST st = new ST("    <funcsList:{func | def test_<func>(self):\r\n}>");
        st.add("funcsList", funcsList);

        String result = st.render();
        if (printDiagnostics)
            System.out.println(result);
        assertEquals(
                "    def test_free_func_1(self):\r\n" +
                         "    def test_free_func_2(self):\r\n" +
                         "    def test_free_func_3(self):\r\n" +
                         "    def test_free_func_4(self):\r\n",
                result
        );
    }

    @Test
    void stListOfLists() {
        List<List<String>> listOfLists = Arrays.asList(
                Arrays.asList("One", "Two", "Three"),
                Arrays.asList("Four", "Five"),
                Arrays.asList("Six", "Seven", "Eight", "Nine")
        );

        String template = "<list :{ items |<items :{ item |<item> }><\\n>}>";
        ST st = new ST(template);
        st.add("list", listOfLists);

        String result = st.render();
        if (printDiagnostics)
            System.out.println(result);
        assertEquals(
                "One Two Three \r\n" +
                        "Four Five \r\n" +
                        "Six Seven Eight Nine \r\n",
                result
        );
    }

    @Test
    void stMapOfList() {
        HashMap<String, List<String>> myMap = new HashMap<>();
        myMap.put("2010", new ArrayList<>());
        myMap.get("2010").add("Item 1");
        myMap.get("2010").add("Item 2");
        myMap.put("2011", new ArrayList<>());
        myMap.get("2011").add("Item 9");
        myMap.put("2012", new ArrayList<>());
        myMap.get("2012").add("Item 6");

        String s =
                "<ul>\n" +
                        "$x.keys:{\n" +
                        "k | <li>$k$</li>\n" +
                        "  <ul>\n" +
                        "    <li>$x.(k);separator=\"</li>\n" +
                        "    <li>\"$</li>\n" +
                        "  </ul>\n" +
                        "}$</ul>";
        ST st = new ST(s, '$', '$');
        st.add("x", myMap);

        String result = st.render();
        if (printDiagnostics)
            System.out.println(result);
    }

    @Test
    void stMapOfList2() {
        HashMap<String, List<String>> myMap = new HashMap<>();
        myMap.put("2010", new ArrayList<>());
        myMap.get("2010").add("Item 1");
        myMap.get("2010").add("Item 2");
        myMap.put("2011", new ArrayList<>());
        myMap.get("2011").add("Item 9");
        myMap.put("2012", new ArrayList<>());
        myMap.get("2012").add("Item 6");

        String s =
                "\r\n" +
                        "<x.keys:{\r\n" +
                        "k | <k>\r\n" +
                        "    <x.(k);separator=\"\r\n" +
                        "\">\r\n" +
                        "}>";
        ST st = new ST(s);
        st.add("x", myMap);

        String result = st.render();
        if (printDiagnostics)
            System.out.println(result);
    }

    @Test
    void stMapOfList3() {
        HashMap<String, ArrayList<String>> classMap = new HashMap<>();
        classMap.put("Silly1", new ArrayList<>());
        classMap.get("Silly1").add("class_func1_get");
        classMap.get("Silly1").add("class_func1_set");
        classMap.put("Silly2", new ArrayList<>());
        classMap.get("Silly2").add("class_func2_get");
        classMap.get("Silly2").add("class_func2_set");
        classMap.put("Silly3", new ArrayList<>());
        classMap.get("Silly3").add("class_func3_get");
        classMap.get("Silly3").add("class_func3_set");

        String s =
                "\r\n" +
                        "<classMap.keys:{\r\n" +
                        "className | class <className>\r\n" +
                        "    method: <classMap.(className);separator=\";\r\n\"" +
                        ">;\r\n" +
                        "}>";
        ST st = new ST(s);
        st.add("classMap", classMap);

        String result = st.render();
        if (printDiagnostics)
            System.out.println(result);
    }

    @Test
    void stSomeLogicInClient() {
        HashMap<String, ArrayList<String>> classMap = new HashMap<>();
        classMap.put("Silly1", new ArrayList<>());
        classMap.get("Silly1").add("class_func1_get");
        classMap.get("Silly1").add("class_func1_set");
        classMap.put("Silly2", new ArrayList<>());
        classMap.get("Silly2").add("class_func2_get");
        classMap.get("Silly2").add("class_func2_set");
        classMap.put("Silly3", new ArrayList<>());
        classMap.get("Silly3").add("class_func3_get");
        classMap.get("Silly3").add("class_func3_set");

        String classUtc = "";
        for (String className : classMap.keySet()) {
            ST stClass = new ST(UtcTemplates.classDefPart);
            stClass.add("className", className);
            String newClass = stClass.render();
            classUtc += newClass;
            for (String classFunctionName: classMap.get(className)) {
                ST stFunction = new ST(UtcTemplates.classFunctionPart);
                stFunction.add("classFunctionName", classFunctionName);
                String newFunction = stFunction.render();
                classUtc += newFunction;
            }
        }

        if (printDiagnostics)
            System.out.println(classUtc);
    }
}
