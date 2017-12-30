// Generated from C:/github/Utils2/Parsing/parsing-utils2/check-python27-manual/Grammar/Antlr\Python27.g4 by ANTLR 4.7
package Grammar.Gen;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link Python27Parser}.
 */
public interface Python27Listener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link Python27Parser#single_input}.
	 * @param ctx the parse tree
	 */
	void enterSingle_input(Python27Parser.Single_inputContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#single_input}.
	 * @param ctx the parse tree
	 */
	void exitSingle_input(Python27Parser.Single_inputContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#file_input}.
	 * @param ctx the parse tree
	 */
	void enterFile_input(Python27Parser.File_inputContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#file_input}.
	 * @param ctx the parse tree
	 */
	void exitFile_input(Python27Parser.File_inputContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#eval_input}.
	 * @param ctx the parse tree
	 */
	void enterEval_input(Python27Parser.Eval_inputContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#eval_input}.
	 * @param ctx the parse tree
	 */
	void exitEval_input(Python27Parser.Eval_inputContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#decorator}.
	 * @param ctx the parse tree
	 */
	void enterDecorator(Python27Parser.DecoratorContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#decorator}.
	 * @param ctx the parse tree
	 */
	void exitDecorator(Python27Parser.DecoratorContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#decorators}.
	 * @param ctx the parse tree
	 */
	void enterDecorators(Python27Parser.DecoratorsContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#decorators}.
	 * @param ctx the parse tree
	 */
	void exitDecorators(Python27Parser.DecoratorsContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#decorated}.
	 * @param ctx the parse tree
	 */
	void enterDecorated(Python27Parser.DecoratedContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#decorated}.
	 * @param ctx the parse tree
	 */
	void exitDecorated(Python27Parser.DecoratedContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#funcdef}.
	 * @param ctx the parse tree
	 */
	void enterFuncdef(Python27Parser.FuncdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#funcdef}.
	 * @param ctx the parse tree
	 */
	void exitFuncdef(Python27Parser.FuncdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#parameters}.
	 * @param ctx the parse tree
	 */
	void enterParameters(Python27Parser.ParametersContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#parameters}.
	 * @param ctx the parse tree
	 */
	void exitParameters(Python27Parser.ParametersContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#varargslist}.
	 * @param ctx the parse tree
	 */
	void enterVarargslist(Python27Parser.VarargslistContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#varargslist}.
	 * @param ctx the parse tree
	 */
	void exitVarargslist(Python27Parser.VarargslistContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#fpdef}.
	 * @param ctx the parse tree
	 */
	void enterFpdef(Python27Parser.FpdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#fpdef}.
	 * @param ctx the parse tree
	 */
	void exitFpdef(Python27Parser.FpdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#fplist}.
	 * @param ctx the parse tree
	 */
	void enterFplist(Python27Parser.FplistContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#fplist}.
	 * @param ctx the parse tree
	 */
	void exitFplist(Python27Parser.FplistContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#stmt}.
	 * @param ctx the parse tree
	 */
	void enterStmt(Python27Parser.StmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#stmt}.
	 * @param ctx the parse tree
	 */
	void exitStmt(Python27Parser.StmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#simple_stmt}.
	 * @param ctx the parse tree
	 */
	void enterSimple_stmt(Python27Parser.Simple_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#simple_stmt}.
	 * @param ctx the parse tree
	 */
	void exitSimple_stmt(Python27Parser.Simple_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#small_stmt}.
	 * @param ctx the parse tree
	 */
	void enterSmall_stmt(Python27Parser.Small_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#small_stmt}.
	 * @param ctx the parse tree
	 */
	void exitSmall_stmt(Python27Parser.Small_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#expr_stmt}.
	 * @param ctx the parse tree
	 */
	void enterExpr_stmt(Python27Parser.Expr_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#expr_stmt}.
	 * @param ctx the parse tree
	 */
	void exitExpr_stmt(Python27Parser.Expr_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#augassign}.
	 * @param ctx the parse tree
	 */
	void enterAugassign(Python27Parser.AugassignContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#augassign}.
	 * @param ctx the parse tree
	 */
	void exitAugassign(Python27Parser.AugassignContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#print_stmt}.
	 * @param ctx the parse tree
	 */
	void enterPrint_stmt(Python27Parser.Print_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#print_stmt}.
	 * @param ctx the parse tree
	 */
	void exitPrint_stmt(Python27Parser.Print_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#del_stmt}.
	 * @param ctx the parse tree
	 */
	void enterDel_stmt(Python27Parser.Del_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#del_stmt}.
	 * @param ctx the parse tree
	 */
	void exitDel_stmt(Python27Parser.Del_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#pass_stmt}.
	 * @param ctx the parse tree
	 */
	void enterPass_stmt(Python27Parser.Pass_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#pass_stmt}.
	 * @param ctx the parse tree
	 */
	void exitPass_stmt(Python27Parser.Pass_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#flow_stmt}.
	 * @param ctx the parse tree
	 */
	void enterFlow_stmt(Python27Parser.Flow_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#flow_stmt}.
	 * @param ctx the parse tree
	 */
	void exitFlow_stmt(Python27Parser.Flow_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#break_stmt}.
	 * @param ctx the parse tree
	 */
	void enterBreak_stmt(Python27Parser.Break_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#break_stmt}.
	 * @param ctx the parse tree
	 */
	void exitBreak_stmt(Python27Parser.Break_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#continue_stmt}.
	 * @param ctx the parse tree
	 */
	void enterContinue_stmt(Python27Parser.Continue_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#continue_stmt}.
	 * @param ctx the parse tree
	 */
	void exitContinue_stmt(Python27Parser.Continue_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#return_stmt}.
	 * @param ctx the parse tree
	 */
	void enterReturn_stmt(Python27Parser.Return_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#return_stmt}.
	 * @param ctx the parse tree
	 */
	void exitReturn_stmt(Python27Parser.Return_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#yield_stmt}.
	 * @param ctx the parse tree
	 */
	void enterYield_stmt(Python27Parser.Yield_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#yield_stmt}.
	 * @param ctx the parse tree
	 */
	void exitYield_stmt(Python27Parser.Yield_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#raise_stmt}.
	 * @param ctx the parse tree
	 */
	void enterRaise_stmt(Python27Parser.Raise_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#raise_stmt}.
	 * @param ctx the parse tree
	 */
	void exitRaise_stmt(Python27Parser.Raise_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#import_stmt}.
	 * @param ctx the parse tree
	 */
	void enterImport_stmt(Python27Parser.Import_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#import_stmt}.
	 * @param ctx the parse tree
	 */
	void exitImport_stmt(Python27Parser.Import_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#import_name}.
	 * @param ctx the parse tree
	 */
	void enterImport_name(Python27Parser.Import_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#import_name}.
	 * @param ctx the parse tree
	 */
	void exitImport_name(Python27Parser.Import_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#import_from}.
	 * @param ctx the parse tree
	 */
	void enterImport_from(Python27Parser.Import_fromContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#import_from}.
	 * @param ctx the parse tree
	 */
	void exitImport_from(Python27Parser.Import_fromContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#import_as_name}.
	 * @param ctx the parse tree
	 */
	void enterImport_as_name(Python27Parser.Import_as_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#import_as_name}.
	 * @param ctx the parse tree
	 */
	void exitImport_as_name(Python27Parser.Import_as_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#dotted_as_name}.
	 * @param ctx the parse tree
	 */
	void enterDotted_as_name(Python27Parser.Dotted_as_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#dotted_as_name}.
	 * @param ctx the parse tree
	 */
	void exitDotted_as_name(Python27Parser.Dotted_as_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#import_as_names}.
	 * @param ctx the parse tree
	 */
	void enterImport_as_names(Python27Parser.Import_as_namesContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#import_as_names}.
	 * @param ctx the parse tree
	 */
	void exitImport_as_names(Python27Parser.Import_as_namesContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#dotted_as_names}.
	 * @param ctx the parse tree
	 */
	void enterDotted_as_names(Python27Parser.Dotted_as_namesContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#dotted_as_names}.
	 * @param ctx the parse tree
	 */
	void exitDotted_as_names(Python27Parser.Dotted_as_namesContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#dotted_name}.
	 * @param ctx the parse tree
	 */
	void enterDotted_name(Python27Parser.Dotted_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#dotted_name}.
	 * @param ctx the parse tree
	 */
	void exitDotted_name(Python27Parser.Dotted_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#global_stmt}.
	 * @param ctx the parse tree
	 */
	void enterGlobal_stmt(Python27Parser.Global_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#global_stmt}.
	 * @param ctx the parse tree
	 */
	void exitGlobal_stmt(Python27Parser.Global_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#exec_stmt}.
	 * @param ctx the parse tree
	 */
	void enterExec_stmt(Python27Parser.Exec_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#exec_stmt}.
	 * @param ctx the parse tree
	 */
	void exitExec_stmt(Python27Parser.Exec_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#assert_stmt}.
	 * @param ctx the parse tree
	 */
	void enterAssert_stmt(Python27Parser.Assert_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#assert_stmt}.
	 * @param ctx the parse tree
	 */
	void exitAssert_stmt(Python27Parser.Assert_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#compound_stmt}.
	 * @param ctx the parse tree
	 */
	void enterCompound_stmt(Python27Parser.Compound_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#compound_stmt}.
	 * @param ctx the parse tree
	 */
	void exitCompound_stmt(Python27Parser.Compound_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#if_stmt}.
	 * @param ctx the parse tree
	 */
	void enterIf_stmt(Python27Parser.If_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#if_stmt}.
	 * @param ctx the parse tree
	 */
	void exitIf_stmt(Python27Parser.If_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#while_stmt}.
	 * @param ctx the parse tree
	 */
	void enterWhile_stmt(Python27Parser.While_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#while_stmt}.
	 * @param ctx the parse tree
	 */
	void exitWhile_stmt(Python27Parser.While_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#for_stmt}.
	 * @param ctx the parse tree
	 */
	void enterFor_stmt(Python27Parser.For_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#for_stmt}.
	 * @param ctx the parse tree
	 */
	void exitFor_stmt(Python27Parser.For_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#try_stmt}.
	 * @param ctx the parse tree
	 */
	void enterTry_stmt(Python27Parser.Try_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#try_stmt}.
	 * @param ctx the parse tree
	 */
	void exitTry_stmt(Python27Parser.Try_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#with_stmt}.
	 * @param ctx the parse tree
	 */
	void enterWith_stmt(Python27Parser.With_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#with_stmt}.
	 * @param ctx the parse tree
	 */
	void exitWith_stmt(Python27Parser.With_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#with_item}.
	 * @param ctx the parse tree
	 */
	void enterWith_item(Python27Parser.With_itemContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#with_item}.
	 * @param ctx the parse tree
	 */
	void exitWith_item(Python27Parser.With_itemContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#except_clause}.
	 * @param ctx the parse tree
	 */
	void enterExcept_clause(Python27Parser.Except_clauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#except_clause}.
	 * @param ctx the parse tree
	 */
	void exitExcept_clause(Python27Parser.Except_clauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#suite}.
	 * @param ctx the parse tree
	 */
	void enterSuite(Python27Parser.SuiteContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#suite}.
	 * @param ctx the parse tree
	 */
	void exitSuite(Python27Parser.SuiteContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#testlist_safe}.
	 * @param ctx the parse tree
	 */
	void enterTestlist_safe(Python27Parser.Testlist_safeContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#testlist_safe}.
	 * @param ctx the parse tree
	 */
	void exitTestlist_safe(Python27Parser.Testlist_safeContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#old_test}.
	 * @param ctx the parse tree
	 */
	void enterOld_test(Python27Parser.Old_testContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#old_test}.
	 * @param ctx the parse tree
	 */
	void exitOld_test(Python27Parser.Old_testContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#old_lambdef}.
	 * @param ctx the parse tree
	 */
	void enterOld_lambdef(Python27Parser.Old_lambdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#old_lambdef}.
	 * @param ctx the parse tree
	 */
	void exitOld_lambdef(Python27Parser.Old_lambdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#test}.
	 * @param ctx the parse tree
	 */
	void enterTest(Python27Parser.TestContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#test}.
	 * @param ctx the parse tree
	 */
	void exitTest(Python27Parser.TestContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#or_test}.
	 * @param ctx the parse tree
	 */
	void enterOr_test(Python27Parser.Or_testContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#or_test}.
	 * @param ctx the parse tree
	 */
	void exitOr_test(Python27Parser.Or_testContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#and_test}.
	 * @param ctx the parse tree
	 */
	void enterAnd_test(Python27Parser.And_testContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#and_test}.
	 * @param ctx the parse tree
	 */
	void exitAnd_test(Python27Parser.And_testContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#not_test}.
	 * @param ctx the parse tree
	 */
	void enterNot_test(Python27Parser.Not_testContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#not_test}.
	 * @param ctx the parse tree
	 */
	void exitNot_test(Python27Parser.Not_testContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#comparison}.
	 * @param ctx the parse tree
	 */
	void enterComparison(Python27Parser.ComparisonContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#comparison}.
	 * @param ctx the parse tree
	 */
	void exitComparison(Python27Parser.ComparisonContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#comp_op}.
	 * @param ctx the parse tree
	 */
	void enterComp_op(Python27Parser.Comp_opContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#comp_op}.
	 * @param ctx the parse tree
	 */
	void exitComp_op(Python27Parser.Comp_opContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#expr}.
	 * @param ctx the parse tree
	 */
	void enterExpr(Python27Parser.ExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#expr}.
	 * @param ctx the parse tree
	 */
	void exitExpr(Python27Parser.ExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#xor_expr}.
	 * @param ctx the parse tree
	 */
	void enterXor_expr(Python27Parser.Xor_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#xor_expr}.
	 * @param ctx the parse tree
	 */
	void exitXor_expr(Python27Parser.Xor_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#and_expr}.
	 * @param ctx the parse tree
	 */
	void enterAnd_expr(Python27Parser.And_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#and_expr}.
	 * @param ctx the parse tree
	 */
	void exitAnd_expr(Python27Parser.And_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#shift_expr}.
	 * @param ctx the parse tree
	 */
	void enterShift_expr(Python27Parser.Shift_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#shift_expr}.
	 * @param ctx the parse tree
	 */
	void exitShift_expr(Python27Parser.Shift_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#arith_expr}.
	 * @param ctx the parse tree
	 */
	void enterArith_expr(Python27Parser.Arith_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#arith_expr}.
	 * @param ctx the parse tree
	 */
	void exitArith_expr(Python27Parser.Arith_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#term}.
	 * @param ctx the parse tree
	 */
	void enterTerm(Python27Parser.TermContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#term}.
	 * @param ctx the parse tree
	 */
	void exitTerm(Python27Parser.TermContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#factor}.
	 * @param ctx the parse tree
	 */
	void enterFactor(Python27Parser.FactorContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#factor}.
	 * @param ctx the parse tree
	 */
	void exitFactor(Python27Parser.FactorContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#power}.
	 * @param ctx the parse tree
	 */
	void enterPower(Python27Parser.PowerContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#power}.
	 * @param ctx the parse tree
	 */
	void exitPower(Python27Parser.PowerContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#atom}.
	 * @param ctx the parse tree
	 */
	void enterAtom(Python27Parser.AtomContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#atom}.
	 * @param ctx the parse tree
	 */
	void exitAtom(Python27Parser.AtomContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#listmaker}.
	 * @param ctx the parse tree
	 */
	void enterListmaker(Python27Parser.ListmakerContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#listmaker}.
	 * @param ctx the parse tree
	 */
	void exitListmaker(Python27Parser.ListmakerContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#testlist_comp}.
	 * @param ctx the parse tree
	 */
	void enterTestlist_comp(Python27Parser.Testlist_compContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#testlist_comp}.
	 * @param ctx the parse tree
	 */
	void exitTestlist_comp(Python27Parser.Testlist_compContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#lambdef}.
	 * @param ctx the parse tree
	 */
	void enterLambdef(Python27Parser.LambdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#lambdef}.
	 * @param ctx the parse tree
	 */
	void exitLambdef(Python27Parser.LambdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#trailer}.
	 * @param ctx the parse tree
	 */
	void enterTrailer(Python27Parser.TrailerContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#trailer}.
	 * @param ctx the parse tree
	 */
	void exitTrailer(Python27Parser.TrailerContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#subscriptlist}.
	 * @param ctx the parse tree
	 */
	void enterSubscriptlist(Python27Parser.SubscriptlistContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#subscriptlist}.
	 * @param ctx the parse tree
	 */
	void exitSubscriptlist(Python27Parser.SubscriptlistContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#subscript}.
	 * @param ctx the parse tree
	 */
	void enterSubscript(Python27Parser.SubscriptContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#subscript}.
	 * @param ctx the parse tree
	 */
	void exitSubscript(Python27Parser.SubscriptContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#sliceop}.
	 * @param ctx the parse tree
	 */
	void enterSliceop(Python27Parser.SliceopContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#sliceop}.
	 * @param ctx the parse tree
	 */
	void exitSliceop(Python27Parser.SliceopContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#exprlist}.
	 * @param ctx the parse tree
	 */
	void enterExprlist(Python27Parser.ExprlistContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#exprlist}.
	 * @param ctx the parse tree
	 */
	void exitExprlist(Python27Parser.ExprlistContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#testlist}.
	 * @param ctx the parse tree
	 */
	void enterTestlist(Python27Parser.TestlistContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#testlist}.
	 * @param ctx the parse tree
	 */
	void exitTestlist(Python27Parser.TestlistContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#dictorsetmaker}.
	 * @param ctx the parse tree
	 */
	void enterDictorsetmaker(Python27Parser.DictorsetmakerContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#dictorsetmaker}.
	 * @param ctx the parse tree
	 */
	void exitDictorsetmaker(Python27Parser.DictorsetmakerContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#classdef}.
	 * @param ctx the parse tree
	 */
	void enterClassdef(Python27Parser.ClassdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#classdef}.
	 * @param ctx the parse tree
	 */
	void exitClassdef(Python27Parser.ClassdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#arglist}.
	 * @param ctx the parse tree
	 */
	void enterArglist(Python27Parser.ArglistContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#arglist}.
	 * @param ctx the parse tree
	 */
	void exitArglist(Python27Parser.ArglistContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#argument}.
	 * @param ctx the parse tree
	 */
	void enterArgument(Python27Parser.ArgumentContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#argument}.
	 * @param ctx the parse tree
	 */
	void exitArgument(Python27Parser.ArgumentContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#list_iter}.
	 * @param ctx the parse tree
	 */
	void enterList_iter(Python27Parser.List_iterContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#list_iter}.
	 * @param ctx the parse tree
	 */
	void exitList_iter(Python27Parser.List_iterContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#list_for}.
	 * @param ctx the parse tree
	 */
	void enterList_for(Python27Parser.List_forContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#list_for}.
	 * @param ctx the parse tree
	 */
	void exitList_for(Python27Parser.List_forContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#list_if}.
	 * @param ctx the parse tree
	 */
	void enterList_if(Python27Parser.List_ifContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#list_if}.
	 * @param ctx the parse tree
	 */
	void exitList_if(Python27Parser.List_ifContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#comp_iter}.
	 * @param ctx the parse tree
	 */
	void enterComp_iter(Python27Parser.Comp_iterContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#comp_iter}.
	 * @param ctx the parse tree
	 */
	void exitComp_iter(Python27Parser.Comp_iterContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#comp_for}.
	 * @param ctx the parse tree
	 */
	void enterComp_for(Python27Parser.Comp_forContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#comp_for}.
	 * @param ctx the parse tree
	 */
	void exitComp_for(Python27Parser.Comp_forContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#comp_if}.
	 * @param ctx the parse tree
	 */
	void enterComp_if(Python27Parser.Comp_ifContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#comp_if}.
	 * @param ctx the parse tree
	 */
	void exitComp_if(Python27Parser.Comp_ifContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#testlist1}.
	 * @param ctx the parse tree
	 */
	void enterTestlist1(Python27Parser.Testlist1Context ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#testlist1}.
	 * @param ctx the parse tree
	 */
	void exitTestlist1(Python27Parser.Testlist1Context ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#yield_expr}.
	 * @param ctx the parse tree
	 */
	void enterYield_expr(Python27Parser.Yield_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#yield_expr}.
	 * @param ctx the parse tree
	 */
	void exitYield_expr(Python27Parser.Yield_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#str}.
	 * @param ctx the parse tree
	 */
	void enterStr(Python27Parser.StrContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#str}.
	 * @param ctx the parse tree
	 */
	void exitStr(Python27Parser.StrContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#number}.
	 * @param ctx the parse tree
	 */
	void enterNumber(Python27Parser.NumberContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#number}.
	 * @param ctx the parse tree
	 */
	void exitNumber(Python27Parser.NumberContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python27Parser#integer}.
	 * @param ctx the parse tree
	 */
	void enterInteger(Python27Parser.IntegerContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python27Parser#integer}.
	 * @param ctx the parse tree
	 */
	void exitInteger(Python27Parser.IntegerContext ctx);
}