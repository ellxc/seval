import ast
from collections import namedtuple

UnaryOp = namedtuple('UnaryOp', ['evaluate', 'pprint'])

UNARY_OPS = {
    ast.Invert: UnaryOp(
        evaluate=lambda env, eval_fn, a: ~eval_fn(a, env),
        pprint=lambda str_fn, a: "~" + str_fn(a),
    ),

    ast.Not: UnaryOp(
        evaluate=lambda env, eval_fn, a: not eval_fn(a, env),
        pprint=lambda str_fn, a: "not " + str_fn(a),
    ),

    ast.UAdd: UnaryOp(
        evaluate=lambda env, eval_fn, a: +eval_fn(a, env),
        pprint=lambda str_fn, a: "+" + str_fn(a),
    ),

    ast.USub: UnaryOp(
        evaluate=lambda env, eval_fn, a: -eval_fn(a, env),
        pprint=lambda str_fn, a: "-" + str_fn(a),
    ),
}
