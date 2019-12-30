import ast
from collections import namedtuple

from .evals import eval_expr, str_expr, eval_assign, eval_augassign, eval_annassign, eval_del, str_del
from .Lambda import Function

Stmt = namedtuple('Stmt', ['evaluate', 'pprint'])

stmts = {
    ast.FunctionDef: Stmt(
        evaluate=lambda env, node: env.update([(node.name,Function(node, env))]) ,
        pprint=lambda node: repr(Function(node)),
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

    ast.Delete     : Stmt(
        evaluate=eval_del,
        pprint=str_del,
    )

}
