import ast
from collections import namedtuple


def eval_comp(env, eval_fn, left, ops, comparators):
    comparisons = zip([left] + comparators, ops, comparators)
    return all(COMPARATOR_OPS[type(op)].evaluate(env, eval_fn, left, right) for left, op, right in comparisons)

def print_comp(str_fn, left, ops, comparators):
    l = str_fn(left)
    rs = []
    for op, c in zip(ops, comparators):
        COMPARATOR_OPS[type(op)].pprint(str_fn, op) + str_fn(c)
    r = "".join(rs)

ComparatorOp = namedtuple('ComparatorOp', ['evaluate', 'pprint'])

COMPARATOR_OPS = {
    ast.Eq: ComparatorOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) == eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + " == " + str_fn(b),
    ),
    ast.NotEq: ComparatorOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) != eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + " != " + str_fn(b),
    ),
    ast.Lt: ComparatorOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) < eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + " < " + str_fn(b),
    ),
    ast.LtE: ComparatorOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) <= eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + " <= " + str_fn(b),
    ),
    ast.Gt: ComparatorOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) > eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + " > " + str_fn(b),
    ),
    ast.GtE: ComparatorOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) >= eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + " >= " + str_fn(b),
    ),
    ast.Is: ComparatorOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) is eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + " is " + str_fn(b),
    ),
    ast.IsNot: ComparatorOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) is not eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + " is not " + str_fn(b),
    ),
    ast.In: ComparatorOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) in eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + " in " + str_fn(b),
    ),
    ast.NotIn: ComparatorOp(
        evaluate=lambda env, eval_fn, a, b: eval_fn(a, env) not in eval_fn(b, env),
        pprint=lambda str_fn, a, b: str_fn(a) + " not in " + str_fn(b),
    ),
}