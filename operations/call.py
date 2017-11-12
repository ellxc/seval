from operations import Lambda
from operations import expr


def call(func, args, keywords, env):
    args2 = [expr.eval_expr(arg, env) for arg in args]
    kwargs2 = {keyword.arg: expr.eval_expr(keyword.value, env) for keyword in keywords}
    func2 = expr.eval_expr(func, env)
    if isinstance(func2, Lambda.Lambda):
        return func2(*args2, __env__=env, **kwargs2)
    else:
        return func2(*args2, **kwargs2)
