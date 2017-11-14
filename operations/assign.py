import ast

from operations import bind


def eval_augassign(env, eval_fn, target, op, value):
    val_ = ast.BinOp(left=target, op=op, right=value)
    return eval_assign(env, eval_fn, [target], val_)


def eval_assign(env, eval_fn, targets, value):
    val = eval_fn(value, env)
    for x in targets:
        if isinstance(x, ast.Attribute):
            if x.attr.startswith("_"):
                raise Exception("access to private fields is disallowed")
            setattr(eval_fn(x.value, env), x.attr, val)
        elif isinstance(x, ast.Name):
            env[x.id] = val
        elif isinstance(x, ast.Subscript):
            if isinstance(x.slice, ast.Index):
                eval_fn(x.value, env)[eval_fn(x.slice.value, env)] = val
            elif isinstance(x.slice, ast.Slice):
                eval_fn(x.value, env)[
                    slice(eval_fn(x.slice.lower, env), eval_fn(x.slice.upper, env),
                          eval_fn(x.slice.step, env))] = val
        else:
            bind.bind(x, val, env)
    return env


def eval_del(env, eval_fn, targets):
    for x in targets:
        if isinstance(x, ast.Attribute):
            if x.attr.startswith("_"):
                raise Exception("access to private fields is disallowed")
            delattr(eval_fn(x.value, env), x.attr)
        elif isinstance(x, ast.Name):
            env.pop(x.id)
        elif isinstance(x, ast.Subscript):
            if isinstance(x.slice, ast.Index):
                del eval_fn(x.value, env)[eval_fn(x.slice.value, env)]
            elif isinstance(x.slice, ast.Slice):
                del eval_fn(x.value, env)[
                    slice(eval_fn(x.slice.lower, env), eval_fn(x.slice.upper, env),
                          eval_fn(x.slice.step, env))]
    return env
