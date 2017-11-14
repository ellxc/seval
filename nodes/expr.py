import ast
from collections import namedtuple

from .Lambda import Lambda
from .evals import eval_expr, str_expr, eval_boolop, str_boolop, eval_op, str_op, eval_unaryop, str_unaryop, \
    eval_comprehensions, str_comprehensions, eval_slice, str_slice, eval_call, str_call, eval_cmpop, str_cmpop


def raise_(text):
    raise Exception(text)


def Raise_(exc, arg):
    raise exc(arg)




Expr = namedtuple('Expr', ['evaluate', 'pprint'])

exprs = {
    ast.BinOp       : Expr(
        evaluate=lambda env, node: eval_op(env, node),
        pprint=lambda str_fn, node: "(" + str_op(node) + ")",
    ),

    ast.UnaryOp     : Expr(
        evaluate=lambda env, node: eval_unaryop(env, node),
        pprint=lambda node: str_unaryop(node),
    ),

    ast.BoolOp      : Expr(
        evaluate=lambda env, node: eval_boolop(env, node),
        pprint=lambda node: str_boolop(node),
    ),

    ast.Compare     : Expr(
        evaluate=eval_cmpop,
        pprint=str_cmpop,
    ),

    ast.Name        : Expr(
        evaluate=lambda env, node: env[node.id] if node.id in env else
        Raise_(NameError, "name '%s' is not defined" % node.id),
        pprint=lambda node: node.id,
    ),

    ast.NameConstant: Expr(
        evaluate=lambda env, node: node.value,
        pprint=lambda node: str(node.value),
    ),

    ast.Num         : Expr(
        evaluate=lambda env, node: node.n,
        pprint=lambda node: str(node.n),
    ),

    ast.Str         : Expr(
        evaluate=lambda env, node: node.s,
        pprint=lambda node: "'" + node.s + "'",
    ),

    ast.List        : Expr(
        evaluate=lambda env, node: list(eval_expr(env, elt) for elt in node.elts),
        pprint=lambda node: "[" + ", ".join(map(str_expr, node.elts)) + "]",
    ),

    ast.Set         : Expr(
        evaluate=lambda env, node: {eval_expr(env, elt) for elt in node.elts},
        pprint=lambda node: "{" + ", ".join(map(str_expr, node.elts)) + "}",
    ),

    ast.Tuple       : Expr(
        evaluate=lambda env, node: tuple(eval_expr(env, elt) for elt in node.elts),
        pprint=lambda node: "(" + ", ".join(map(str_expr, node.elts)) + ")",
    ),

    ast.Dict        : Expr(
        evaluate=lambda env, node:
        {eval_expr(env, key): eval_expr(env, value) for key, value in zip(node.keys, node.values)},
        pprint=lambda node: "{" + ", ".join(str_expr(key) + ":" +
                                            str_expr(value) for key, value in zip(node.keys, node.values)) + "}",
    ),

    ast.Lambda      : Expr(
        evaluate=lambda env, node: Lambda(node),
        pprint=lambda node: "lambda " + ",".join(
            [x.arg for y in dict(ast.iter_fields(node.args)).values() if y for x in y]) + ": " + str_expr(node.body),
    ),

    ast.Attribute   : Expr(
        evaluate=lambda env, eval_fn, value, attr, ctx:
        (getattr(eval_fn(value, env), attr) if isinstance(value, ast.Attribute) else getattr(eval_fn(value, env), attr))
        if not attr.startswith("__") else raise_("access to private fields is disallowed"),
        pprint=lambda str_fn, value, attr, ctx: str_fn(value) + "." + attr
    ),

    ast.Call        : Expr(
        evaluate=lambda env, node: eval_call(env, node),
        pprint=lambda node: str_call(node),
    ),

    ast.ListComp    : Expr(
        evaluate=lambda env, node: [eval_expr(genenv, node.elt) for genenv in
                                    eval_comprehensions(env, node.generators)],
        pprint=lambda node: "[" + str_expr(node.elt) + " for " + str_comprehensions(node.generators) + "]",
    ),

    ast.DictComp    : Expr(
        evaluate=lambda env, node:
        {eval_expr(genenv, node.key): eval_expr(genenv, node.value) for genenv in
         eval_comprehensions(env, node.generators)},
        pprint=lambda node:
        "{" + str_expr(node.key) + ":" + str_expr(node.value) + " for " + str_comprehensions(node.generators) + "}",
    ),

    ast.SetComp     : Expr(
        evaluate=lambda env, node:
        {eval_expr(genenv, node.elt) for genenv in eval_comprehensions(env, node.generators)},
        pprint=lambda node: "{" + str_expr(node.elt) + " for " + str_comprehensions(node.generators) + "}",
    ),

    ast.GeneratorExp: Expr(
        evaluate=lambda env, node: (eval_expr(genenv, node.elt) for genenv in
                                    eval_comprehensions(env, node.generators)),
        pprint=lambda node: "(" + str_expr(node.elt) + " for " + str_comprehensions(node.generators) + ")",
    ),

    ast.Subscript   : Expr(
        evaluate=lambda env, node: eval_expr(env, node.value)[eval_slice(env, node.slice)],
        pprint=lambda node: str_expr(node.value) + "[" + str_slice(node.slice) + "]"
    ),

    ast.IfExp       : Expr(
        evaluate=lambda env, eval_fn, test, body, orelse:
        eval_fn(body, env) if eval_fn(test, env) else eval_fn(orelse, env),
        pprint=lambda str_fn, test, body, orelse: str_fn(body) + " if " + str_fn(test) + " else " + str_fn(orelse),
    ),
}
