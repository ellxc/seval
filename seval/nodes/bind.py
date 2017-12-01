import ast


def bind_name(id, ctx, rhs, env):
    env[id] = rhs


def bind_iter(elts, ctx, rhs, env):
    for elt, subrhs in zip(elts, rhs):
        bind(elt, subrhs, env)


def bind_arg(arg, annotation, rhs, env):
    env[arg] = rhs


binds = {
    ast.Name : bind_name,
    ast.List : bind_iter,
    ast.Tuple: bind_iter,
    ast.arg  : bind_arg,
}


def bind(node, rhs, env):
    binds[type(node)](rhs=rhs, env=env, **dict(ast.iter_fields(node)))
    return env
