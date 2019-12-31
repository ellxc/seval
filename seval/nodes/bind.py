import ast


def bind_name(id, ctx, rhs, env):
    env[id] = rhs



def bind_iter(elts, ctx, rhs, env):
    stars = sum(map(lambda x: isinstance(x, ast.Starred), elts))

    if stars > 1:
        raise SyntaxError("two starred expressions in assignment")
    elif stars:
        try:
            irhs = iter(rhs)
            ielts = iter(elts)
            starred = []
            while not starred:
                x = next(ielts)
                if isinstance(x, ast.Starred):
                    starred = list(irhs)
                    bind(x.value, starred, env)
                    break
                else:
                    bind(x, next(irhs), env)
            for x in reversed(list(ielts)):
                bind(x, starred.pop(), env)
        except IndexError:
            raise ValueError("not enough values to unpack (expected at least %d, got %d)" % (len(elts)-stars, len(rhs)))
    else:
        if len(elts) != len(rhs):
            raise ValueError("not enough values to unpack (expected %d, got %d)" % (len(elts), len(rhs)))
        for elt, subrhs in zip(elts, rhs):
            bind(elt, subrhs, env)


def bind_arg(arg, annotation, rhs, env, type_comment=None):
    env[arg] = rhs


def bind_star(*_, **__):
    raise SyntaxError("starred assignment target must be in a list or tuple")


binds = {
    ast.Name: bind_name,
    ast.List: bind_iter,
    ast.Tuple: bind_iter,
    ast.arg: bind_arg,
    ast.Starred: bind_star,
}


def bind(node, rhs, env):
    binds[type(node)](rhs=rhs, env=env, **dict(ast.iter_fields(node)))
    return env
