/* Python 2.7.X ANTLR 4 grammar */

/*
 * The MIT License (MIT)
 *
 * Copyright (c) 2014 by Bart Kiers
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 *
 * Project      : python3-parser; an ANTLR4 grammar for Python 3
 *                https://github.com/bkiers/python3-parser
 * Developed by : Bart Kiers, bart@big-o.nl
 */

/*
 * Python 2.7.X ANTLR 4 grammar
 * ----------------------------
 * ANTLR 4 grammar for Python 2.7. Based specifically on the full
 * grammar defined for 2.7.13 and the Python 3.3 ATNTLR 4 grammer
 * from Kiers (see above).
 *                                       Dave Karetnyk, June 2017
 */

grammar Python27;

// All comments that start with "///" are copy-pasted from The Python Language Reference
//      https://docs.python.org/2/reference/grammar.html

tokens { INDENT, DEDENT }

@lexer::members {

  // A queue where extra tokens are pushed on (see the NEWLINE lexer rule).
  private java.util.LinkedList<Token> tokens = new java.util.LinkedList<>();

  // The stack that keeps track of the indentation level.
  private java.util.Stack<Integer> indents = new java.util.Stack<>();

  // The amount of opened braces, brackets and parenthesis.
  private int opened = 0;

  // The most recently produced token.
  private Token lastToken = null;

  @Override
  public void emit(Token t) {
    super.setToken(t);
    tokens.offer(t);
  }

  @Override
  public Token nextToken() {

    // Check if the end-of-file is ahead and there are still some DEDENTS expected.
    if (_input.LA(1) == EOF && !this.indents.isEmpty()) {

      // Remove any trailing EOF tokens from our buffer.
      for (int i = tokens.size() - 1; i >= 0; i--) {
        if (tokens.get(i).getType() == EOF) {
          tokens.remove(i);
        }
      }

      // First emit an extra line break that serves as the end of the statement.
      this.emit(commonToken(Python27Parser.NEWLINE, "\n"));

      // Now emit as much DEDENT tokens as needed.
      while (!indents.isEmpty()) {
        this.emit(createDedent());
        indents.pop();
      }

      // Put the EOF back on the token stream.
      this.emit(commonToken(Python27Parser.EOF, "<EOF>"));
    }

    Token next = super.nextToken();

    if (next.getChannel() == Token.DEFAULT_CHANNEL) {
      // Keep track of the last token on the default channel.
      this.lastToken = next;
    }

    return tokens.isEmpty() ? next : tokens.poll();
  }

  private Token createDedent() {
    CommonToken dedent = commonToken(Python27Parser.DEDENT, "");
    dedent.setLine(this.lastToken.getLine());
    return dedent;
  }

  private CommonToken commonToken(int type, String text) {
    int stop = this.getCharIndex() - 1;
    int start = text.isEmpty() ? stop : stop - text.length() + 1;
    return new CommonToken(this._tokenFactorySourcePair, type, DEFAULT_TOKEN_CHANNEL, start, stop);
  }

  // Calculates the indentation of the provided spaces, taking the
  // following rules into account:
  //
  // "Tabs are replaced (from left to right) by one to eight spaces
  //  such that the total number of characters up to and including
  //  the replacement is a multiple of eight [...]"
  //
  //  -- https://docs.python.org/3.1/reference/lexical_analysis.html#indentation
  static int getIndentationCount(String spaces) {

    int count = 0;

    for (char ch : spaces.toCharArray()) {
      switch (ch) {
        case '\t':
          count += 8 - (count % 8);
          break;
        default:
          // A normal space char.
          count++;
      }
    }

    return count;
  }

  boolean atStartOfInput() {
    return super.getCharPositionInLine() == 0 && super.getLine() == 1;
  }
}

/*
 * -----------------------------------------------------------------------------------------------
 * PARSER RULES
 */

/// Start symbols for the grammar:
///     ingle_input is a single interactive statement;
///     file_input is a module or sequence of commands read from an input file;
///     eval_input is the input for the eval() and input() functions.
/// NB: compound_stmt in single_input is followed by extra NEWLINE!

/// single_input: NEWLINE | simple_stmt | compound_stmt NEWLINE
single_input
    :   NEWLINE
    |   simple_stmt
    |   compound_stmt NEWLINE
    ;

/// file_input: (NEWLINE | stmt)* ENDMARKER
file_input
    :   (   NEWLINE
        |   stmt
        )*
        EOF
    ;

/// eval_input: testlist NEWLINE* ENDMARKER
eval_input
    :   testlist NEWLINE* EOF
    ;

/// decorator: '@' dotted_name [ '(' [arglist] ')' ] NEWLINE
decorator
    :   '@' dotted_name ( '(' arglist? ')' )? NEWLINE
    ;

/// decorators: decorator+
decorators
    :   decorator+
    ;

/// decorated: decorators (classdef | funcdef)
decorated
    :   decorators  (   classdef
                    |   funcdef
                    )
    ;

/// funcdef: 'def' NAME parameters ':' suite
funcdef
    :   DEF NAME parameters ':' suite
    ;

/// parameters: '(' [varargslist] ')'
parameters
    :   '(' varargslist? ')'
    ;

/// varargslist: ((fpdef ['=' test] ',')*
///              ('*' NAME [',' '**' NAME] | '**' NAME) |
///              fpdef ['=' test] (',' fpdef ['=' test])* [','])
varargslist
    :   (   ( fpdef ( '=' test )? ',' )* ( '*' NAME ( ',' '**' NAME )? | '**' NAME )
            |   fpdef ( '=' test)? ( ',' fpdef ( '=' test)? )* ( ',' )?
        )
    ;

/// fpdef: NAME | '(' fplist ')'
fpdef
    :   NAME
    |   '(' fplist ')'
    ;

/// fplist: fpdef (',' fpdef)* [',']
fplist
    :   fpdef ( ',' fpdef )* ','?
    ;

/// stmt: simple_stmt | compound_stmt
stmt
    :   simple_stmt
    |   compound_stmt
    ;

/// simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE
simple_stmt
    :   small_stmt ( ';' small_stmt )* ';'? NEWLINE
    ;

/// small_stmt: (expr_stmt | print_stmt  | del_stmt | pass_stmt | flow_stmt |
///             import_stmt | global_stmt | exec_stmt | assert_stmt)
small_stmt
    :   expr_stmt
    |   print_stmt
    |   del_stmt
    |   pass_stmt
    |   flow_stmt
    |   import_stmt
    |   global_stmt
    |   exec_stmt
    |   assert_stmt
    ;

/// expr_stmt: testlist (augassign (yield_expr|testlist) |
///                     ('=' (yield_expr|testlist))*)
expr_stmt
    :   testlist    (   augassign ( yield_expr | testlist )
                    |   ( '=' ( yield_expr | testlist ) )*
                    )
    ;

/// augassign: ('+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=' |
///             '<<=' | '>>=' | '**=' | '//=')
augassign
    :   '+='
    |   '-='
    |   '*='
    |   '/='
    |   '%='
    |   '&='
    |   '|='
    |   '^='
    |   '<<='
    |   '>>='
    |   '**='
    |   '//='
    ;

/// print_stmt: 'print' ( [ test (',' test)* [','] ] |
///                      '>>' test [ (',' test)+ [','] ] )
print_stmt
    :   PRINT   (   ( test ( ',' test)* ','? )?
                |   '>>' test ( ( ',' test )+ ','? )?
                )
    ;

/// del_stmt: 'del' exprlist
del_stmt
    :   DEL exprlist
    ;

/// pass_stmt: 'pass'
pass_stmt
    :   PASS
    ;

/// flow_stmt: break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt
flow_stmt
    :   break_stmt
    |   continue_stmt
    |   return_stmt
    |   raise_stmt
    |   yield_stmt
    ;

/// break_stmt: 'break'
break_stmt
    :   BREAK
    ;

/// continue_stmt: 'continue'
continue_stmt
    :   CONTINUE
    ;

/// return_stmt: 'return' [testlist]
return_stmt
    :   RETURN testlist?
    ;

/// yield_stmt: yield_expr
yield_stmt
    :   yield_expr
    ;

/// raise_stmt: 'raise' [test [',' test [',' test]]]
raise_stmt
    :   RAISE ( test ( ',' test ( ',' test )? )? )?
    ;

/// import_stmt: import_name | import_from
import_stmt
    :   import_name
    |   import_from
    ;

/// import_name: 'import' dotted_as_names
import_name
    :   IMPORT dotted_as_names
    ;

/// import_from: ('from' ('.'* dotted_name | '.'+)
///               'import' ('*' | '(' import_as_names ')' | import_as_names))
import_from
    :   FROM    (   '.'* dotted_name
                |   '.'+
                )
        IMPORT  (   '*'
                |   '(' import_as_names ')'
                |   import_as_names
                )
    ;

/// import_as_name: NAME ['as' NAME]
import_as_name
    :    NAME ( AS NAME )?
    ;

/// dotted_as_name: dotted_name ['as' NAME]
dotted_as_name
    :   dotted_name ( AS NAME )?
    ;

/// import_as_names: import_as_name (',' import_as_name)* [',']
import_as_names
    :   import_as_name ( ',' import_as_name )* ','?
    ;

/// dotted_as_names: dotted_as_name (',' dotted_as_name)*
dotted_as_names
    :   dotted_as_name ( ',' dotted_as_name )*
    ;

/// dotted_name: NAME ('.' NAME)*
dotted_name
    :   NAME ( '.' NAME )*
    ;

/// global_stmt: 'global' NAME (',' NAME)*
global_stmt
    :   GLOBAL NAME ( ',' NAME )*
    ;

/// exec_stmt: 'exec' expr ['in' test [',' test]]
exec_stmt
    :   EXEC expr ( IN test ( ',' test )? )?
    ;

/// assert_stmt: 'assert' test [',' test]
assert_stmt
    :   ASSERT test ( ',' test )?
    ;

/// compound_stmt: if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef | decorated
compound_stmt
    :   if_stmt
    |   while_stmt
    |   for_stmt
    |   try_stmt
    |   with_stmt
    |   funcdef
    |   classdef
    |   decorated
    ;

/// if_stmt: 'if' test ':' suite ('elif' test ':' suite)* ['else' ':' suite]
if_stmt
    :   IF test ':' suite ( ELIF test ':' suite )* ( ELSE ':' suite )?
    ;

/// while_stmt: 'while' test ':' suite ['else' ':' suite]
while_stmt
    :   WHILE test ':' suite ( ELSE ':' suite )?
    ;

/// for_stmt: 'for' exprlist 'in' testlist ':' suite ['else' ':' suite]
for_stmt
    :   FOR exprlist IN testlist ':' suite ( ELSE ':' suite )?
    ;

/// try_stmt: ('try' ':' suite
///            ((except_clause ':' suite)+
///       ['else' ':' suite]
///       ['finally' ':' suite] |
///      'finally' ':' suite))
try_stmt
    :   TRY ':' suite   (   ( except_clause ':' suite )+
                            ( ELSE ':' suite )?
                            ( FINALLY ':' suite )?
                        |   FINALLY ':' suite
                        )
    ;

/// with_stmt: 'with' with_item (',' with_item)*  ':' suite
with_stmt
    :   WITH with_item ( ',' with_item )* ':' suite
    ;

/// with_item: test ['as' expr]
with_item
    :   test ( AS expr )?
    ;

/// # NB compile.c makes sure that the default except clause is last
/// except_clause: 'except' [test [('as' | ',') test]]
except_clause
    :   EXCEPT ( test ( ( 'as' | ',') test )? )?
    ;

/// suite: simple_stmt | NEWLINE INDENT stmt+ DEDENT
suite
    :   simple_stmt
        |   NEWLINE INDENT stmt+ DEDENT
    ;

/// ----------------------------------------------------------------
/// Backward compatibility cruft to support:
///     [ x for x in lambda: True, lambda: False if x() ]
/// even while also allowing:
///     lambda x: 5 if x else 2
/// But not a mix of the two.
/// testlist_safe: old_test [(',' old_test)+ [',']]
testlist_safe
    :   old_test ( ( ',' old_test )+ ','? )?
    ;

/// old_test: or_test | old_lambdef
old_test
    :   or_test
    |   old_lambdef
    ;

/// old_lambdef: 'lambda' [varargslist] ':' old_test
old_lambdef
    :   LAMBDA ( varargslist )? ':' old_test
    ;
/// end backward compatibility cruft
/// ----------------------------------------------------------------

/// test: or_test ['if' or_test 'else' test] | lambdef
test
    :   or_test ( IF or_test ELSE test )?
    |   lambdef
    ;

/// or_test: and_test ('or' and_test)*
or_test
    :   and_test ( OR and_test )*
    ;

/// and_test: not_test ('and' not_test)*
and_test
    :   not_test ( AND not_test )*
    ;

/// not_test: 'not' not_test | comparison
not_test
    :   NOT not_test
    |   comparison
    ;

/// comparison: expr (comp_op expr)*
comparison
    :   expr ( comp_op expr )*
    ;

/// # <> isn't actually a valid comparison operator in Python. It's here for the
/// # sake of a __future__ import described in PEP 401
/// comp_op: '<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'not' 'in'|'is'|'is' 'not'
comp_op
    :   '<'
    |   '>'
    |   '=='
    |   '>='
    |   '<='
    |   '<>'
    |   '!='
    |   IN
    |   NOT IN
    |   IS
    |   IS NOT
    ;

/// expr: xor_expr ('|' xor_expr)*
expr
    :   xor_expr ( '|' xor_expr )*
    ;

/// xor_expr: and_expr ('^' and_expr)*
xor_expr
    :   and_expr ( '^' and_expr )*
    ;

/// and_expr: shift_expr ('&' shift_expr)*
and_expr
    :   shift_expr ( '&' shift_expr )*
    ;

/// shift_expr: arith_expr (('<<'|'>>') arith_expr)*
shift_expr
    :   arith_expr  (   '<<' arith_expr
                    |   '>>' arith_expr
                    )*
    ;

/// arith_expr: term (('+'|'-') term)*
arith_expr
    :   term    (   '+' term
                |   '-' term
                )*
    ;

/// term: factor (('*'|'/'|'%'|'//') factor)*
term
    :   factor  (   '*' factor
                |   '/' factor
                |   '%' factor
                |   '//' factor
                |   '@' factor // PEP 465
                )*
    ;

/// factor: ('+'|'-'|'~') factor | power
factor
    :   '+' factor
    |   '-' factor
    |   '~' factor
    |   power
    ;

/// power: atom trailer* ['**' factor]
power
    :   atom trailer* ( '**' factor )?
    ;

/// atom: ('(' [yield_expr|testlist_comp] ')' |
///        '[' [listmaker] ']' |
///        '{' [dictorsetmaker] '}' |
///        '`' testlist1 '`' |
///        NAME | NUMBER | STRING+)
// Appended NONE, TRUE, and FALSE: 2.7.13 full grammar does not specify this. Seems like an error
// becuse, e.g., the 3.3.6 full grammar does have these present.
atom
    :   '(' (   yield_expr
            |   testlist_comp
            )?
        ')'
        |   '[' listmaker? ']'
        |   '{' dictorsetmaker? '}'
        |   '`' testlist1 '`'
        |   NAME
        |   number
        |   str+
        |   NONE
        |   TRUE
        |   FALSE
    ;

/// listmaker: test ( list_for | (',' test)* [','] )
listmaker
    :   test    (   list_for
                |  ( ',' test )* ','?
                )
    ;

/// testlist_comp: test ( comp_for | (',' test)* [','] )
testlist_comp
    :   test    (   comp_for
                |   ( ',' test )* ','?
                )
    ;

/// lambdef: 'lambda' [varargslist] ':' test
lambdef
    : LAMBDA varargslist? ':' test
    ;

/// trailer: '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME
trailer
    :   '(' arglist? ')'
        |   '[' subscriptlist ']'
        |   '.' NAME
    ;

/// subscriptlist: subscript (',' subscript)* [',']
subscriptlist
    :   subscript ( ',' subscript )* ','?
    ;

/// subscript: '.' '.' '.' | test | [test] ':' [test] [sliceop]
subscript
    :   ELLIPSIS
        |   test
        |   test? ':' test? sliceop?
    ;

/// sliceop: ':' [test]
sliceop
    :   ':' test?
    ;

/// exprlist: expr (',' expr)* [',']
exprlist
    :   expr ( ',' expr )* ','?
    ;

/// testlist: test (',' test)* [',']
testlist
    :   test ( ',' test )* ','?
    ;

/// dictorsetmaker: ( (test ':' test (comp_for | (',' test ':' test)* [','])) |
///                   (test (comp_for | (',' test)* [','])) )
dictorsetmaker
    :   test ':' test   (   comp_for
                        |   ( ',' test ':' test )* ','?
                        )
        |   test    (   comp_for
                    |   ( ',' test )* ','?
                    )
    ;

// Type in 2.7.13 grammar - below should be 'arglist', not 'testlist'.
/// classdef: 'class' NAME ['(' [testlist] ')'] ':' suite
classdef
    :   CLASS NAME ( '(' arglist? ')' )? ':' suite
    ;

/// arglist: (argument ',')* (argument [',']
///                          |'*' test (',' argument)* [',' '**' test]
///                          |'**' test)
arglist
    :   ( argument ',' )*   (   argument ','?
                            |   '*' test ( ',' argument )* ( ',' '**' test )?
                            |   '**' test
                            )
    ;

/// The reason that keywords are test nodes instead of NAME is that using NAME
/// results in an ambiguity. ast.c makes sure it's a NAME.
///     argument: test [comp_for] | test '=' test  # Really [keyword '='] test
argument
    :   test comp_for?
        |   test '=' test
    ;

/// list_iter: list_for | list_if
list_iter
    :   list_for
        |   list_if
    ;

/// list_for: 'for' exprlist 'in' testlist_safe [list_iter]
list_for
    :   FOR exprlist IN testlist_safe list_iter?
    ;

/// list_if: 'if' old_test [list_iter]
list_if
    :   IF old_test list_iter?
    ;

/// comp_iter: comp_for | comp_if
comp_iter
    :   comp_for
        |   comp_if
    ;

/// comp_for: 'for' exprlist 'in' or_test [comp_iter]
comp_for
    :   FOR exprlist IN or_test comp_iter?
    ;

/// comp_if: 'if' old_test [comp_iter]
comp_if
    :   IF old_test comp_iter?
    ;

///testlist1: test (',' test)*
testlist1
    :   test ( ',' test )*
    ;

/// yield_expr: 'yield' [testlist]
yield_expr
    :   YIELD testlist?
    ;

str
    :   STRING_LITERAL
    |   BYTES_LITERAL
    ;

number
    :   integer
    |   FLOAT_NUMBER
    |   IMAG_NUMBER
    ;

/// integer        ::=  decimalinteger | octinteger | hexinteger | bininteger
// integer or 'long integer'  possible: see use of LONG_POSTFIX fragment definition.
integer
    :   DECIMAL_INTEGER
    |   OCT_INTEGER
    |   HEX_INTEGER
    |   BIN_INTEGER
    ;

/*
 * -----------------------------------------------------------------------------------------------
 * LEXER RULES
 */

DEF         : 'def';
RETURN      : 'return';
RAISE       : 'raise';
FROM        : 'from';
IMPORT      : 'import';
AS          : 'as';
GLOBAL      : 'global';
EXEC        : 'exec';
ASSERT      : 'assert';
IF          : 'if';
ELIF        : 'elif';
ELSE        : 'else';
WHILE       : 'while';
FOR         : 'for';
IN          : 'in';
TRY         : 'try';
FINALLY     : 'finally';
WITH        : 'with';
EXCEPT      : 'except';
LAMBDA      : 'lambda';
OR          : 'or';
AND         : 'and';
NOT         : 'not';
IS          : 'is';
NONE        : 'None';
TRUE        : 'True';
FALSE       : 'False';
CLASS       : 'class';
YIELD       : 'yield';
DEL         : 'del';
PASS        : 'pass';
CONTINUE    : 'continue';
BREAK       : 'break';
PRINT       : 'print';

NEWLINE
    :   (   {atStartOfInput()}?   SPACES
        |   ( '\r'? '\n' | '\r' | '\f' ) SPACES?
        )
   {
     String newLine = getText().replaceAll("[^\r\n\f]+", "");
     String spaces = getText().replaceAll("[\r\n\f]+", "");
     int next = _input.LA(1);

     if (opened > 0 || next == '\r' || next == '\n' || next == '\f' || next == '#') {
       // If we're inside a list or on a blank line, ignore all indents, 
       // dedents and line breaks.
       skip();
     }
     else {
       emit(commonToken(NEWLINE, newLine));

       int indent = getIndentationCount(spaces);
       int previous = indents.isEmpty() ? 0 : indents.peek();

       if (indent == previous) {
         // skip indents of the same size as the present indent-size
         skip();
       }
       else if (indent > previous) {
         indents.push(indent);
         emit(commonToken(Python27Parser.INDENT, spaces));
       }
       else {
         // Possibly emit more than 1 DEDENT token.
         while(!indents.isEmpty() && indents.peek() > indent) {
           this.emit(createDedent());
           indents.pop();
         }
       }
     }
   }
 ;

/// identifier   ::=  id_start id_continue*
NAME
    :   ID_START ID_CONTINUE*
    ;

/// stringliteral   ::=  [stringprefix](shortstring | longstring)
/// stringprefix    ::=  "r" | "R"
STRING_LITERAL
    :   [uU]? [rR]? ( SHORT_STRING | LONG_STRING )
    ;

/// bytesliteral   ::=  bytesprefix(shortbytes | longbytes)
/// bytesprefix    ::=  "b" | "B" | "br" | "Br" | "bR" | "BR"
BYTES_LITERAL
    :   [bB] [rR]? ( SHORT_BYTES | LONG_BYTES )
    ;

/// decimalinteger ::=  nonzerodigit digit* | "0"+
DECIMAL_INTEGER
    :   NON_ZERO_DIGIT DIGIT* LONG_POSTFIX?
    |   '0'+ LONG_POSTFIX?
    ;

/// octinteger     ::=  "0" ("o" | "O") octdigit+ | "0" octdigit+
OCT_INTEGER
    :   '0' [oO] OCT_DIGIT+ LONG_POSTFIX?
    |   '0' OCT_DIGIT+ LONG_POSTFIX?
    ;

/// hexinteger     ::=  "0" ("x" | "X") hexdigit+
HEX_INTEGER
    :   '0' [xX] HEX_DIGIT+ LONG_POSTFIX?
    ;

/// bininteger     ::=  "0" ("b" | "B") bindigit+
BIN_INTEGER
    :   '0' [bB] BIN_DIGIT+ LONG_POSTFIX?
    ;

/// floatnumber   ::=  pointfloat | exponentfloat
FLOAT_NUMBER
    :   POINT_FLOAT
    |   EXPONENT_FLOAT
    ;

/// imagnumber ::=  (floatnumber | intpart) ("j" | "J")
IMAG_NUMBER
    :   ( FLOAT_NUMBER | INT_PART ) [jJ]
    ;

DOT                 : '.';
ELLIPSIS            : '...';
STAR                : '*';
OPEN_PAREN          : '(' {opened++;};
CLOSE_PAREN         : ')' {opened--;};
COMMA               : ',';
COLON               : ':';
SEMI_COLON          : ';';
POWER               : '**';
ASSIGN              : '=';
OPEN_BRACK          : '[' {opened++;};
CLOSE_BRACK         : ']' {opened--;};
OR_OP               : '|';
XOR                 : '^';
AND_OP              : '&';
LEFT_SHIFT          : '<<';
RIGHT_SHIFT         : '>>';
ADD                 : '+';
MINUS               : '-';
DIV                 : '/';
MOD                 : '%';
IDIV                : '//';
NOT_OP              : '~';
OPEN_BRACE          : '{' {opened++;};
CLOSE_BRACE         : '}' {opened--;};
LESS_THAN           : '<';
GREATER_THAN        : '>';
EQUALS              : '==';
GT_EQ               : '>=';
LT_EQ               : '<=';
NOT_EQ_1            : '<>';
NOT_EQ_2            : '!=';
AT                  : '@';
ARROW               : '->';
ADD_ASSIGN          : '+=';
SUB_ASSIGN          : '-=';
MULT_ASSIGN         : '*=';
AT_ASSIGN           : '@=';
DIV_ASSIGN          : '/=';
MOD_ASSIGN          : '%=';
AND_ASSIGN          : '&=';
OR_ASSIGN           : '|=';
XOR_ASSIGN          : '^=';
LEFT_SHIFT_ASSIGN   : '<<=';
RIGHT_SHIFT_ASSIGN  : '>>=';
POWER_ASSIGN        : '**=';
IDIV_ASSIGN         : '//=';

SKIP_
    : ( SPACES | COMMENT | LINE_JOINING ) -> skip
    ;

UNKNOWN_CHAR
    : .
    ;

/* 
 * -----------------------------------------------------------------------------------------------
 * fragments
 */

/// shortstring     ::=  "'" shortstringitem* "'" | '"' shortstringitem* '"'
/// shortstringitem ::=  shortstringchar | stringescapeseq
/// shortstringchar ::=  <any source character except "\" or newline or the quote>
fragment SHORT_STRING
    : '\'' ( STRING_ESCAPE_SEQ | ~[\\\r\n\f'] )* '\''
    | '"' ( STRING_ESCAPE_SEQ | ~[\\\r\n\f"] )* '"'
    ;

/// longstring      ::=  "'''" longstringitem* "'''" | '"""' longstringitem* '"""'
fragment LONG_STRING
    : '\'\'\'' LONG_STRING_ITEM*? '\'\'\''
    | '"""' LONG_STRING_ITEM*? '"""'
    ;

/// longstringitem  ::=  longstringchar | stringescapeseq
fragment LONG_STRING_ITEM
    : LONG_STRING_CHAR
    | STRING_ESCAPE_SEQ
    ;

/// longstringchar  ::=  <any source character except "\">
fragment LONG_STRING_CHAR
    : ~'\\'
    ;

/// stringescapeseq ::=  "\" <any source character>
fragment STRING_ESCAPE_SEQ
    : '\\' .
    ;

// Needed in 2.7 grammar to indicate 'long integer'. For 3.0 and later everything is long so was
// removed.
fragment LONG_POSTFIX
    :   (   'l'
        |   'L'
        )
    ;

/// nonzerodigit   ::=  "1"..."9"
fragment NON_ZERO_DIGIT
    : [1-9]
    ;

/// digit          ::=  "0"..."9"
fragment DIGIT
    : [0-9]
    ;

/// octdigit       ::=  "0"..."7"
fragment OCT_DIGIT
    : [0-7]
    ;

/// hexdigit       ::=  digit | "a"..."f" | "A"..."F"
fragment HEX_DIGIT
    : [0-9a-fA-F]
    ;

/// bindigit       ::=  "0" | "1"
fragment BIN_DIGIT
    : [01]
    ;

/// pointfloat    ::=  [intpart] fraction | intpart "."
fragment POINT_FLOAT
    : INT_PART? FRACTION
    | INT_PART '.'
    ;

/// exponentfloat ::=  (intpart | pointfloat) exponent
fragment EXPONENT_FLOAT
    : ( INT_PART | POINT_FLOAT ) EXPONENT
    ;

/// intpart       ::=  digit+
fragment INT_PART
    : DIGIT+
    ;

/// fraction      ::=  "." digit+
fragment FRACTION
    : '.' DIGIT+
    ;

/// exponent      ::=  ("e" | "E") ["+" | "-"] digit+
fragment EXPONENT
    : [eE] [+-]? DIGIT+
    ;

/// shortbytes     ::=  "'" shortbytesitem* "'" | '"' shortbytesitem* '"'
/// shortbytesitem ::=  shortbyteschar | bytesescapeseq
fragment SHORT_BYTES
    : '\'' ( SHORT_BYTES_CHAR_NO_SINGLE_QUOTE | BYTES_ESCAPE_SEQ )* '\''
    | '"' ( SHORT_BYTES_CHAR_NO_DOUBLE_QUOTE | BYTES_ESCAPE_SEQ )* '"'
    ;
    
/// longbytes      ::=  "'''" longbytesitem* "'''" | '"""' longbytesitem* '"""'
fragment LONG_BYTES
    : '\'\'\'' LONG_BYTES_ITEM*? '\'\'\''
    | '"""' LONG_BYTES_ITEM*? '"""'
    ;

/// longbytesitem  ::=  longbyteschar | bytesescapeseq
fragment LONG_BYTES_ITEM
    : LONG_BYTES_CHAR
    | BYTES_ESCAPE_SEQ
    ;

/// shortbyteschar ::=  <any ASCII character except "\" or newline or the quote>
fragment SHORT_BYTES_CHAR_NO_SINGLE_QUOTE
    : [\u0000-\u0009]
    | [\u000B-\u000C]
    | [\u000E-\u0026]
    | [\u0028-\u005B]
    | [\u005D-\u007F]
    ;

fragment SHORT_BYTES_CHAR_NO_DOUBLE_QUOTE
    : [\u0000-\u0009]
    | [\u000B-\u000C]
    | [\u000E-\u0021]
    | [\u0023-\u005B]
    | [\u005D-\u007F]
    ; 

/// longbyteschar  ::=  <any ASCII character except "\">
fragment LONG_BYTES_CHAR
    : [\u0000-\u005B]
    | [\u005D-\u007F]
    ;

/// bytesescapeseq ::=  "\" <any ASCII character>
fragment BYTES_ESCAPE_SEQ
    : '\\' [\u0000-\u007F]
    ;

fragment SPACES
    : [ \t]+
    ;

fragment COMMENT
    : '#' ~[\r\n\f]*
    ;

fragment LINE_JOINING
    : '\\' SPACES? ( '\r'? '\n' | '\r' | '\f' )
    ;

fragment OTHER_ID_START
    : [\u2118\u212E\u309B\u309C]
    ;

/// id_start     ::=  <all characters in general categories Lu, Ll, Lt, Lm, Lo, Nl, the
/// underscore, and characters with the Other_ID_Start property>
fragment ID_START
    : '_'
    | [\p{Letter}\p{Letter_Number}]
    | OTHER_ID_START
    ;

/// id_continue  ::=  <all characters in id_start, plus characters in the categories Mn, Mc, Nd,
/// Pc and others with the Other_ID_Continue property>
fragment ID_CONTINUE
    : ID_START
    | [\p{Nonspacing_Mark}\p{Spacing_Mark}\p{Decimal_Number}\p{Connector_Punctuation}\p{Format}]
    ;
