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
    return operators[type(node.op)].evaluate(env, node.left, node.right)


def str_op(node: ast.operator):
    return operators[type(node.op)].pprint(node)


def eval_unaryop(env, node: ast.unaryop):
    return unaryops[type(node.op)].evaluate(env, node)


def str_unaryop(node: ast.unaryop):
    return unaryops[type(node.op)].pprint(node)


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


def eval_slice(env, node: ast.slice):
    return slices[type(node)].evaluate(env, node)


def str_slice(node: ast.slice):
    return slices[type(node)].pprint(node)


def eval_call(env, node: ast.Call):
    args = [eval_expr(env, arg) for arg in node.args]
    kwargs = {keyword.arg: eval_expr(env, keyword.value) for keyword in node.keywords}
    func = eval_expr(env, node.func)
    if isinstance(func, Lambda):
        return func(env)(*args, **kwargs)
    else:
        return func(*args, **kwargs)


def str_call(node: ast.Call):
    return str_expr(node.func) + "(" + ", ".join((list(map(str_expr, node.args)) if node.args else []) +
                                                 [a + "=" + str_expr(b) for a, b in
                                                  [(keyword.arg, keyword.value) for keyword in node.keywords]]) + ")"


def eval_assign(env, node: ast.Assign):
    val = eval_expr(env, node.value)
    for x in node.targets:
        if isinstance(x, ast.Attribute):
            if x.attr.startswith("_"):
                raise Exception("access to private fields is disallowed")
            setattr(eval_expr(env, x.value), x.attr, val)
        elif isinstance(x, ast.Subscript):
            eval_expr(env, x.value)[eval_slice(env, x.slice)] = val
        else:
            bind(x, val, env)


def eval_augassign(env, node):
    val_ = ast.Assign(targets=[node.target], value=ast.BinOp(left=node.target, op=node.op, right=node.value))
    return eval_assign(env, val_)


def eval_del(env, node):
    for x in node.targets:
        if isinstance(x, ast.Attribute):
            if x.attr.startswith("_"):
                raise Exception("access to private fields is disallowed")
            delattr(eval_expr(env, x.value), x.attr)
        elif isinstance(x, ast.Name):
            env.pop(x.id)
        elif isinstance(x, ast.Subscript):
            del eval_expr(env, x.value)[eval_slice(x.slice, env)]


def eval_cmpop(env, node):
    comparisons = zip([node.left] + node.comparators, node.ops, node.comparators)
    return all(cmpops[type(op)].evaluate(env, left, right) for left, op, right in comparisons)


def str_cmpop(node):
    l = str_expr(node.left)
    rs = []
    for op, c in zip(node.ops, node.comparators):
        print(op, c, l)
        rs.append(cmpops[type(op)].pprint(node.left, c))
    r = " ".join(rs)
    return r


from nodes.bind import bind
from nodes.boolop import boolops
from nodes.expr import exprs
from nodes.stmt import stmts
from nodes.operator import operators
from nodes.unaryop import unaryops
from nodes.slice import slices
from nodes.Lambda import Lambda
from nodes.cmpops import cmpops
