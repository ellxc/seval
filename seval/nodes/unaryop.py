import ast
from collections import namedtuple

from .evals import eval_expr, str_expr

UnaryOp = namedtuple('UnaryOp', ['evaluate', 'pprint'])

unaryops = {
    ast.Invert: UnaryOp(
        evaluate=lambda env, node: ~eval_expr(env, node),
        pprint=lambda node: "~" + str_expr(node),
    ),

    ast.Not   : UnaryOp(
        evaluate=lambda env, node: not eval_expr(env, node),
        pprint=lambda node: "not " + str_expr(node),
    ),

    ast.UAdd  : UnaryOp(
        evaluate=lambda env, node: +eval_expr(env, node),
        pprint=lambda node: "+" + str_expr(node),
    ),

    ast.USub  : UnaryOp(
        evaluate=lambda env, node: -eval_expr(env, node),
        pprint=lambda node: "-" + str_expr(node),
    ),
}
