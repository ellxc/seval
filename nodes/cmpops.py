import ast
from collections import namedtuple

from .evals import eval_expr, str_expr

ComparatorOp = namedtuple('ComparatorOp', ['evaluate', 'pprint'])

cmpops = {
    ast.Eq   : ComparatorOp(
        evaluate=lambda env, a, b: eval_expr(env, a) == eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + " == " + str_expr(b),
    ),
    ast.NotEq: ComparatorOp(
        evaluate=lambda env, a, b: eval_expr(env, a) != eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + " != " + str_expr(b),
    ),
    ast.Lt   : ComparatorOp(
        evaluate=lambda env, a, b: eval_expr(env, a) < eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + " < " + str_expr(b),
    ),
    ast.LtE  : ComparatorOp(
        evaluate=lambda env, a, b: eval_expr(env, a) <= eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + " <= " + str_expr(b),
    ),
    ast.Gt   : ComparatorOp(
        evaluate=lambda env, a, b: eval_expr(env, a) > eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + " > " + str_expr(b),
    ),
    ast.GtE  : ComparatorOp(
        evaluate=lambda env, a, b: eval_expr(env, a) >= eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + " >= " + str_expr(b),
    ),
    ast.Is   : ComparatorOp(
        evaluate=lambda env, a, b: eval_expr(env, a) is eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + " is " + str_expr(b),
    ),
    ast.IsNot: ComparatorOp(
        evaluate=lambda env, a, b: eval_expr(env, a) is not eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + " is not " + str_expr(b),
    ),
    ast.In   : ComparatorOp(
        evaluate=lambda env, a, b: eval_expr(env, a) in eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + " in " + str_expr(b),
    ),
    ast.NotIn: ComparatorOp(
        evaluate=lambda env, a, b: eval_expr(env, a) not in eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + " not in " + str_expr(b),
    ),
}
