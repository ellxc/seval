import ast


def eval_all(env, node):
    if isinstance(node, ast.stmt):
        pass
    elif isinstance(node, ast.expr):
        pass
    elif isinstance(node, ast.slice):
        pass
    elif isinstance(node, ast.boolop):
        pass
    elif isinstance(node, ast.operator):
        pass
    elif isinstance(node, ast.unaryop):
        pass
    elif isinstance(node, ast.comprehension):
        pass
    elif isinstance(node, ast.excepthandler):
        pass
    elif isinstance(node, ast.arguments):
        pass
    elif isinstance(node, ast.arg):
        pass
    elif isinstance(node, ast.keyword):
        pass
    elif isinstance(node, ast.keyword):
        pass
    elif isinstance(node, ast.alias):
        pass
    elif isinstance(node, ast.withitem):
        pass


def eval_boolop(env, node: ast.boolop):
    return boolops[type(node.op)].evaluate(env, node)


def str_boolop(node: ast.boolop):
    return boolops[type(node).op].pprint(node)


def eval_expr(env, node: ast.expr):
    t = exprs[type(node)].evaluate(env, node)
    # if type(t) is ModuleType and t.__name__ in blacklist or hasattr(t,"__module__") and t.__module__ in blacklist or t.__class__.__module__ in blacklist:
    #     raise Exception("naughty")
    return t


def str_expr(node: ast.expr):
    return exprs[type(node)].pprint(node)


def eval_stmt(env, node: ast.stmt):
    t = stmts[type(node)].evaluate(env, node)
    # if type(t) is ModuleType and t.__name__ in blacklist or hasattr(t,   "__module__") and t.__module__ in blacklist or t.__class__.__module__ in blacklist:
    #     raise Exception("naughty")
    return t


def str_stmt(node: ast.stmt):
    return stmts[type(node)].pprint(node)


def eval_op(env, node: ast.operator):
    return operators[type(node)].evaluate(env, node)


def str_op(node: ast.operator):
    return operators[type(node)].pprint(node)


def eval_unaryop(env, node: ast.unaryop):
    return unaryops[type(node)].evaluate(env, node)


def str_unaryop(node):
    return unaryops[type(node)].pprint(node)


def eval_comprehensions(env, *nodes: ast.comprehension):
    if not nodes:
        yield env
    else:
        [current], *next = nodes
        for it in eval_expr(env, current.iter):
            for genenv in eval_comprehensions(bind(current.target, it, env.copy()), *next):
                if all(eval_expr(genenv, if_) for if_ in current.ifs):
                    yield genenv


def str_comprehensions(*nodes: ast.comprehension):
    return " ".join(str_expr(node.target) + " in " + str_expr(node.iter) +
                    ((" if " + " ".join(str_expr(IF) for IF in node.ifs)) if node.ifs else "") for node in nodes)


def eval_slice(env, node):
    return slices[type(node)].evaluate(env, node)


def str_slice(node):
    return slices[type(node)].pprint(node)


def eval_call(env, node):
    args = [eval_expr(env, arg) for arg in node.args]
    kwargs = {keyword.arg: eval_expr(env, keyword.value) for keyword in node.keywords}
    func = eval_expr(env, node.func)
    if isinstance(func, Lambda):
        return func(env)(*args, **kwargs)
    else:
        return func(*args, **kwargs)


def str_call(node):
    return str_expr(node.func) + "(" + ", ".join((list(map(str_expr, node.args)) if node.args else []) +
                                                 [a + "=" + str_expr(b) for a, b in
                                                  [(keyword.arg, keyword.value) for keyword in node.keywords]]) + ")"


from .bind import bind
from .boolop import boolops
from .expr import exprs
from .stmt import stmts
from .operator import operators
from .unaryop import unaryops
from .slice import slices
from .Lambda import Lambda
