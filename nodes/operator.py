import ast
from collections import namedtuple

from .evals import str_expr, eval_expr

BinOp = namedtuple('BinOp', ['evaluate', 'pprint'])

operators = {
    ast.Add     : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) + eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '+' + str_expr(b),
    ),

    ast.Sub     : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) - eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '-' + str_expr(b),
    ),

    ast.Mult    : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) * eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '*' + str_expr(b),
    ),

    ast.Div     : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) / eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '/' + str_expr(b),
    ),

    ast.Mod     : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) % eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '%' + str_expr(b)
    ),

    ast.Pow     : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) ** eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '**' + str_expr(b)
    ),

    ast.LShift  : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) << eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '<<' + str_expr(b)
    ),

    ast.RShift  : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) >> eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '>>' + str_expr(b)
    ),

    ast.BitOr   : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) | eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '|' + str_expr(b)
    ),

    ast.BitXor  : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) ^ eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '^' + str_expr(b)
    ),

    ast.BitAnd  : BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) & eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '&' + str_expr(b)
    ),

    ast.FloorDiv: BinOp(
        evaluate=lambda env, a, b: eval_expr(env, a) // eval_expr(env, b),
        pprint=lambda a, b: str_expr(a) + '//' + str_expr(b)
    ),
}
