import ast
from collections import namedtuple

from .evals import eval_expr, str_expr, eval_assign, eval_augassign

Stmt = namedtuple('Stmt', ['evaluate', 'pprint'])

stmts = {
    ast.FunctionDef: Stmt(
        evaluate=lambda env, node: node.name,
        pprint=lambda node: node.name,
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
    )

}
