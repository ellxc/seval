import ast
from collections import namedtuple

BinOp = namedtuple('BinOp', ['evaluate', 'pprint'])

operators = {
    ast.Add: BinOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) + eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + '+' + str_fn(b),
    ),

    ast.Sub: BinOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) - eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + '-' + str_fn(b),
    ),

    ast.Mult: BinOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) * eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + '*' + str_fn(b),
    ),

    ast.Div: BinOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) / eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + '/' + str_fn(b),
    ),

    ast.Mod: BinOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) % eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + '%' + str_fn(b)
    ),

    ast.Pow: BinOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) ** eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + '**' + str_fn(b)
    ),

    ast.LShift: BinOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) << eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + '<<' + str_fn(b)
    ),

    ast.RShift: BinOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) >> eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + '>>' + str_fn(b)
    ),

    ast.BitOr: BinOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) | eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + '|' + str_fn(b)
    ),

    ast.BitXor: BinOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) ^ eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + '^' + str_fn(b)
    ),

    ast.BitAnd: BinOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) & eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + '&' + str_fn(b)
    ),

    ast.FloorDiv: BinOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) // eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + '//' + str_fn(b)
    ),
}

