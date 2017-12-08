from collections import namedtuple
from .evals import *
from .Lambda import Lambda

def raise_(text):
    raise Exception(text)


def Raise_(exc, arg):
    raise exc(arg)


Expr = namedtuple('Expr', ['evaluate', 'pprint'])

exprs = {
    ast.BinOp: Expr(
        evaluate=lambda env, node: eval_op(env, node),
        pprint=lambda str_fn, node: "(" + str_op(node) + ")",
    ),

    ast.UnaryOp: Expr(
        evaluate=lambda env, node: eval_unaryop(env, node),
        pprint=lambda node: str_unaryop(node),
    ),

    ast.BoolOp: Expr(
        evaluate=lambda env, node: eval_boolop(env, node),
        pprint=lambda node: str_boolop(node),
    ),

    ast.Compare: Expr(
        evaluate=eval_cmpop,
        pprint=str_cmpop,
    ),

    ast.Name: Expr(
        evaluate=lambda env, node: eval_name(env, node),
        pprint=lambda node: node.id,
    ),

    ast.NameConstant: Expr(
        evaluate=lambda env, node: node.value,
        pprint=lambda node: str(node.value),
    ),

    ast.Num: Expr(
        evaluate=lambda env, node: node.n,
        pprint=lambda node: str(node.n),
    ),

    ast.Str: Expr(
        evaluate=lambda env, node: node.s,
        pprint=lambda node: "'" + node.s + "'",
    ),

    ast.List: Expr(
        evaluate=lambda env, node: list(eval_expr(env, elt) for elt in node.elts),
        pprint=lambda node: "[" + ", ".join(map(str_expr, node.elts)) + "]",
    ),

    ast.Set: Expr(
        evaluate=lambda env, node: {eval_expr(env, elt) for elt in node.elts},
        pprint=lambda node: "{" + ", ".join(map(str_expr, node.elts)) + "}",
    ),

    ast.Tuple: Expr(
        evaluate=lambda env, node: tuple(eval_expr(env, elt) for elt in node.elts),
        pprint=lambda node: "(" + ", ".join(map(str_expr, node.elts)) + ")",
    ),

    ast.Dict: Expr(
        evaluate=lambda env, node:
        {eval_expr(env, key): eval_expr(env, value) for key, value in zip(node.keys, node.values)},
        pprint=lambda node: "{" + ", ".join(str_expr(key) + ":" +
                                            str_expr(value) for key, value in zip(node.keys, node.values)) + "}",
    ),

    ast.Lambda: Expr(
        evaluate=lambda env, node: Lambda(node),
        pprint=lambda node: "lambda " + ",".join(
            [x.arg for y in dict(ast.iter_fields(node.args)).values() if y for x in y]) + ": " + str_expr(node.body),
    ),

    ast.Attribute: Expr(
        evaluate=lambda env, node: eval_attribute(env, node),
        pprint=lambda str_fn, value, attr, ctx: str_fn(value) + "." + attr
    ),

    ast.Call: Expr(
        evaluate=lambda env, node: eval_call(env, node),
        pprint=lambda node: str_call(node),
    ),

    ast.ListComp: Expr(
        evaluate=lambda env, node: [eval_expr(genenv, node.elt) for genenv in
                                    eval_comprehensions(env, *node.generators)],
        pprint=lambda node: "[" + str_expr(node.elt) + " for " + str_comprehensions(node.generators) + "]",
    ),

    ast.DictComp: Expr(
        evaluate=lambda env, node:
        {eval_expr(genenv, node.key): eval_expr(genenv, node.value) for genenv in
         eval_comprehensions(env, *node.generators)},
        pprint=lambda node:
        "{" + str_expr(node.key) + ":" + str_expr(node.value) + " for " + str_comprehensions(node.generators) + "}",
    ),

    ast.SetComp: Expr(
        evaluate=lambda env, node:
        {eval_expr(genenv, node.elt) for genenv in eval_comprehensions(env, *node.generators)},
        pprint=lambda node: "{" + str_expr(node.elt) + " for " + str_comprehensions(node.generators) + "}",
    ),

    ast.GeneratorExp: Expr(
        evaluate=lambda env, node: (eval_expr(genenv, node.elt) for genenv in
                                    eval_comprehensions(env, *node.generators)),
        pprint=lambda node: "(" + str_expr(node.elt) + " for " + str_comprehensions(node.generators) + ")",
    ),

    ast.Subscript: Expr(
        evaluate=lambda env, node: eval_expr(env, node.value)[eval_slice(env, node.slice)],
        pprint=lambda node: str_expr(node.value) + "[" + str_slice(node.slice) + "]"
    ),

    ast.IfExp: Expr(
        evaluate=lambda env, node:
        eval_expr(env, node.body) if eval_expr(env, node.test) else eval_expr(env, node.orelse),
        pprint=lambda node: str_expr(node.body) + " if " + str_expr(node.test) + " else " + str_expr(node.orelse),
    ),

    ast.JoinedStr: Expr(
        evaluate=lambda env, node: "".join(eval_expr(env, x) for x in node.values),
        pprint=lambda node: "".join(str_expr(x) for x in node.values)
    ),

    ast.FormattedValue: Expr(
        evaluate=lambda env, node: format({-1: lambda x: x, 115: str, 114: repr, 97: ascii}[node.conversion]
                                          (eval_expr(env, node.value)),
                                          eval_expr(env, node.format_spec) if node.format_spec is not None else ""),
        pprint=lambda node: "<fstring>",
    ),

    ast.Starred: Expr(
        evaluate=lambda env, node: eval_starred(env, node),
        pprint=lambda node: "*"+str_expr(node.value)
    ),
}
