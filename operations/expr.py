import ast
from collections import ChainMap
from collections import namedtuple

from operations.Lambda import Lambda
from operations.bin_ops import BIN_OPS
from operations.call import call
from operations.comparator_ops import print_comp, eval_comp
from operations.unary_ops import UNARY_OPS


def eval_expr(node, env):
    if node is not None:
        if type(node) in EXPRS:
            return EXPRS[type(node)].evaluate(**ChainMap({"env": env, "eval_fn": eval_expr}, dict(ast.iter_fields(node))))
        else:
            try:
                raise Exception(ast.dump(node))
            except TypeError:
                raise Exception(node)
    else:
        return None

def str_expr(node):
    if node is not None:
        if type(node) in EXPRS:
            return EXPRS[type(node)].pprint(**ChainMap({"str_fn": str_expr}, dict(ast.iter_fields(node))))
        else:
            try:
                raise Exception(ast.dump(node))
            except TypeError:
                raise Exception(node)
    else:
        return None

def raise_(text):
    raise Exception(text)

Expr = namedtuple('Expr', ['evaluate', 'pprint'])

EXPRS = {
    ast.BinOp: Expr(
        evaluate=lambda env, eval_fn, op, left, right: BIN_OPS[type(op)].evaluate(env, eval_fn, left, right),
        pprint=lambda str_fn, op, left, right: "(" + BIN_OPS[type(op)].pprint(str_fn, left, right) + ")",
    ),

    ast.UnaryOp: Expr(
        evaluate=lambda env, eval_fn, op, operand: UNARY_OPS[type(op)].evaluate(env, eval_fn, operand),
        pprint=lambda str_fn, op, operand: UNARY_OPS[type(op)].pprint(str_fn, op) + str_fn(operand),
    ),

    ast.Compare: Expr(
        evaluate=eval_comp,
        pprint=print_comp,
    ),

    ast.Name: Expr(
        evaluate=lambda env, eval_fn, ctx, id: env[id],
        pprint=lambda str_fn, ctx, id: id,
    ),

    ast.NameConstant: Expr(
        evaluate=lambda env, eval_fn, value: value,
        pprint=lambda str_fn, value: str(value),
    ),

    ast.Num: Expr(
        evaluate=lambda env, eval_fn, n: n,
        pprint=lambda str_fn, n: str(n),
    ),

    ast.Str: Expr(
        evaluate=lambda env, eval_fn, s: s,
        pprint=lambda str_fn, s: "'" + s + "'",
    ),

    ast.List: Expr(
        evaluate=lambda env, eval_fn, ctx, elts: list(eval_fn(elt, env) for elt in elts),
        pprint=lambda str_fn, ctx, elts: "[" + ", ".join(map(str_fn, elts)) + "]",
    ),

    ast.Set: Expr(
        evaluate=lambda env, eval_fn, elts: {eval_fn(elt, env) for elt in elts},
        pprint=lambda str_fn, elts: "{" + ",".join([str_fn(elt) for elt in elts]) + "}",
    ),

    ast.Tuple: Expr(
        evaluate=lambda env, eval_fn, ctx, elts: tuple(eval_fn(elt, env) for elt in elts),
        pprint=lambda str_fn, ctx, elts: "(" + ", ".join([str_fn(elt) for elt in elts]) + ")",
    ),

    ast.Dict: Expr(
        evaluate=lambda env, eval_fn, keys, values: {eval_fn(key, env): eval_fn(value, env) for key, value in
                                                     zip(keys, values)},
        pprint=lambda str_fn, keys, values: "{" + ", ".join([str_fn(key) + ":" +
                                                             str_fn(value) for key, value in zip(keys, values)]) + "}",
    ),

    ast.Lambda: Expr(
        evaluate=lambda env, eval_fn, args, body: Lambda(body, dict(ast.iter_fields(args)), eval_fn, str_expr),
        pprint=lambda str_fn, args, body: "lambda " + ",".join(
            [x.arg for y in dict(ast.iter_fields(args)).values() if y for x in y]) + ": " + str_fn(body),
    ),

    ast.Attribute: Expr(
        evaluate=lambda env, eval_fn, value, attr, ctx:
        (getattr(eval_fn(value, env), attr) if isinstance(value, ast.Attribute) else getattr(eval_fn(value, env), attr))
        if not attr.startswith("_") else raise_("access to private fields is disallowed"),
        pprint=lambda str_fn, value, attr, ctx: str_fn(value) + "." + attr
    ),

    ast.Call: Expr(
        evaluate=lambda env, eval_fn, func, args, keywords: call(func, args, keywords, env),
        pprint=lambda str_fn, func, args, keywords:
        str_fn(func) + "(" + ", ".join(
            (list(map(str_fn, args)) if args else []) + [
                a + "=" + str_fn(b) for a, b in [(keyword.arg, keyword.value) for keyword in keywords]]) + ")",
    )

}
