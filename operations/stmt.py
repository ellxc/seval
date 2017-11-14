import ast
from collections import namedtuple

from .evals import eval_expr, str_expr

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

    # ast.Assign: Stmt(
    #     evaluate=eval_assign,
    #     pprint=lambda str_fn, targets, value: ",".join(map(str_fn, targets)) + "=" + str_fn(value)
    # )

}
