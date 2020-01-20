import ast
from collections import namedtuple

from .evals import eval_expr, str_expr, eval_assign, eval_augassign, eval_annassign, eval_del, str_del, eval_stmt, ret_exception
from .Lambda import Function
from .bind import bind
Stmt = namedtuple('Stmt', ['evaluate', 'pprint'])

LOOP_LIMIT = 10000


def whilestmt(env, node: ast.While, limit=LOOP_LIMIT):
    while eval_expr(env, node.test):
        if limit < 0:
            raise Exception("while loop exceeded operations limit")
        for s in node.body:
            if type(s) is ast.Break:
                break
            elif type(s) is ast.For:
                limit = forstmt(env, s, limit)
            elif type(s) is ast.While:
                limit = whilestmt(env, s, limit)
            else:
                limit -= 1
                eval_stmt(env, s)
        else:
            continue
        break
    else:
        for s in node.orelse:
            limit -= 1
            eval_stmt(env, s)

    return limit


def forstmt(env, node: ast.For, limit=LOOP_LIMIT):
    for it in eval_expr(env, node.iter):
        bind(node.target, it, env)
        for s in node.body:
            if limit < 0:
                raise Exception("for loop exceeded operations limit")
            if type(s) is ast.Break:
                break
            elif type(s) is ast.For:
                limit = forstmt(env, s, limit)
            elif type(s) is ast.While:
                limit = whilestmt(env, s, limit)
            else:
                limit -= 1
                eval_stmt(env, s)
        else:
            continue
        break
    else:
        for s in node.orelse:
            limit -= 1
            eval_stmt(env, s)

    return limit


def ifstmt(env, node: ast.If):
    if eval_expr(env, node.test):
        for s in node.body:
            eval_stmt(env, s)
    else:
        for s in node.orelse:
            eval_stmt(env, s)


def retstmt(env, node: ast.Return):
    raise ret_exception(eval_expr(env, node.value))


stmts = {
    ast.FunctionDef: Stmt(
        evaluate=lambda env, node: env.update([(node.name, Function(node, env))]),
        pprint=lambda node: f"<function def {node.name}>",
    ),

    ast.Expr       : Stmt(
        evaluate=lambda env, node: eval_expr(env, node.value),
        pprint=lambda node: str_expr(node.value),
    ),

    ast.Assign     : Stmt(
        evaluate=eval_assign,
        pprint=lambda node: ",".join(map(str_expr, node.targets)) + "=" + str_expr(node.value)
    ),

    ast.AugAssign  : Stmt(
        evaluate=eval_augassign,
        pprint=lambda node: str_expr(node.target) + "aug=" + str_expr(node.value)
    ),

    ast.AnnAssign: Stmt(
        evaluate=eval_annassign,
        pprint=lambda node: str_expr(node.target)+":type" + (" = %s" % str_expr(node.value) if node.value is not None else "")
    ),

    ast.Delete: Stmt(
        evaluate=eval_del,
        pprint=str_del,
    ),

    ast.While: Stmt(
        evaluate=whilestmt,
        pprint="while!",
    ),

    ast.For: Stmt(
        evaluate=forstmt,
        pprint="for!",
    ),

    ast.If: Stmt(
        evaluate=ifstmt,
        pprint="if",
    ),

    ast.Pass: Stmt(
        evaluate=lambda *x: None,
        pprint="Pass",
    ),

    ast.Return: Stmt(
        evaluate=retstmt,
        pprint="ret",
    )

}
