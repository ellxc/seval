import ast
from collections import namedtuple

Slice = namedtuple('slice', ['evaluate', 'pprint'])

Slices = {
    ast.Slice: Slice(
        evaluate=lambda env, eval_fn, lower, upper, step, value_:
        eval_fn(value_, env)[slice(eval_fn(lower, env), eval_fn(upper, env), eval_fn(step, env))],
        pprint=lambda str_fn, expr, lower, upper, step, value_=None:
        str(expr) + "[" + str_fn(lower) + ((":" + str_fn(upper) + ((":" + str_fn(step)) if step != 1 else ""))
                                           if upper else "") + "]"
    ),
    ast.Index: Slice(
        evaluate=lambda eval_fn, env, value, expr=None, value_=None:
        expr[eval_fn(value, env)] if expr is not None else eval_fn(value_, env)[eval_fn(value, env)],
        pprint=lambda str_fn, value, expr=None, value_=None:
        str(expr) + "[" + str_fn(value) + "]" if expr is not None else str_fn(value_) + "[" + str_fn(value) + "]"
    ),
}
