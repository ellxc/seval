import ast
from collections import namedtuple

from .evals import eval_expr, str_expr

Slice = namedtuple('slice', ['evaluate', 'pprint'])

slices = {
    ast.Slice: Slice(
        evaluate=lambda env, node: slice(eval_expr(env, node.lower), eval_expr(env, node.upper),
                                         eval_expr(env, node.step)),
        pprint=lambda node: str_expr(node.lower) + (
        (":" + str_expr(node.upper) + ((":" + str_expr(node.step)) if node.step != 1 else ""))
        if node.upper else "") + "]"
    ),
    ast.Index: Slice(
        evaluate=lambda env, node: eval_expr(env, node.value),
        pprint=lambda node: str_expr(node.value),
    ),
}
