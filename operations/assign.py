import ast

from operations import expr, bind


def eval_augassign(node, env):
    val_ = ast.BinOp(left=node.target, op=node.op, right=node.value)
    node = ast.Assign(targets=[node.target], value=val_)
    return eval_assign(node, env)


def eval_assign(node, env):
    val = expr.eval_expr(node.value, env)
    for x in node.targets:
        if isinstance(x, ast.Attribute):
            if x.attr.startswith("_"):
                raise Exception("access to private fields is disallowed")
            setattr(expr.eval_expr(x.value, env), x.attr, val)
        elif isinstance(x, ast.Name):
            env[x.id] = val
        elif isinstance(x, ast.Subscript):
            if isinstance(x.slice, ast.Index):
                expr.eval_expr(x.value, env)[expr.eval_expr(x.slice.value, env)] = val
            elif isinstance(x.slice, ast.Slice):
                expr.eval_expr(x.value, env)[
                    slice(expr.eval_expr(x.slice.lower, env), expr.eval_expr(x.slice.upper, env),
                          expr.eval_expr(x.slice.step, env))] = val
        else:
            bind.bind(x, val, env)
    return env


def eval_del(node, env):
    for x in node.targets:
        if isinstance(x, ast.Attribute):
            if x.attr.startswith("_"):
                raise Exception("access to private fields is disallowed")
            delattr(expr.eval_expr(x.value, env), x.attr)
        elif isinstance(x, ast.Name):
            env.pop(x.id)
        elif isinstance(x, ast.Subscript):
            if isinstance(x.slice, ast.Index):
                del expr.eval_expr(x.value, env)[expr.eval_expr(x.slice.value, env)]
            elif isinstance(x.slice, ast.Slice):
                del expr.eval_expr(x.value, env)[
                    slice(expr.eval_expr(x.slice.lower, env), expr.eval_expr(x.slice.upper, env),
                          expr.eval_expr(x.slice.step, env))]
    return env
