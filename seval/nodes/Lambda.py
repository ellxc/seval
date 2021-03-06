import ast
from collections import OrderedDict, ChainMap

from seval.nodes.bind import bind
from .evals import eval_expr, str_expr, eval_stmt, ret_exception

def getenv(funcname, args, vararg, kwarg, defaults, call_args, call_kwargs,
           env, posonlyargs=None, kwonlyargs=None, kw_defaults=None):
    subenv = OrderedDict()

    for param, arg in zip(args, call_args):
        bind(param, arg, subenv)
    varargs = call_args[len(args):]
    if vararg:
        subenv[vararg.arg] = varargs
    elif varargs:
        raise TypeError("%s() takes %s positional arguments but %s %s given" %
                        (funcname, len(args), len(call_args), "was" if len(call_args) == 1 else "were"))
    kwonlyargs_ = []
    kwenv = OrderedDict()
    if kwonlyargs:
        for param in kwonlyargs:
            bind(param, None, kwenv)
            kwonlyargs_.append(param.arg)
    for param in args:
        bind(param, None, kwenv)

    kwargsd = {}
    for key, value in call_kwargs.items():
        if key in subenv:
            raise TypeError("%s() got multiple values for argument '%s'" % key)
        elif key in kwenv:
            subenv[key] = value
        elif key in args:
            subenv[key] = value
        else:
            kwargsd[key] = value
    if kwarg:
        subenv[kwarg.arg] = kwargsd
    elif kwargsd:
        raise TypeError("%s() got an unexpected keyword argument '%s'" % (funcname, list(kwargsd.keys())[0]))

    newenv = OrderedDict()
    if not kwonlyargs:
        for param, default in zip(args[::-1], defaults[::-1]):
            # print(default)
            bind(param, eval_expr(env, default), newenv)
    else:
        for param, default in [(p, d) for p, d in zip(kwonlyargs, kw_defaults)]:
            if default is not None:
                bind(param, default, newenv)
    newenv.update(subenv)
    kwmissing = []
    posmissing = []
    for key in kwenv.keys():
        if key not in newenv:
            if key in kwonlyargs_:
                kwmissing.append(key)
            else:
                posmissing.append(key)
    if posmissing:
        raise TypeError("%s() missing %s required positional argument" % (funcname, len(posmissing)) + "%s: %s" %
                        ("s" if len(posmissing) > 1 else "",
                         "'%s'" % posmissing[0] +
                         ((", " + ", ".join(["'%s'" % x for x in posmissing[1:-1]])) if len(posmissing) > 2 else "") +
                         (" and '%s'" % posmissing[-1] if len(posmissing) > 1 else "")))
    if kwmissing:
        raise TypeError("%s() missing %s required keyword-only argument" % (funcname, len(kwmissing)) + "%s: %s" %
                        ("s" if len(kwmissing) > 1 else "",
                         "'%s'" % kwmissing[0] +
                         ((", " + ", ".join(["'%s'" % x for x in kwmissing[1:-1]])) if len(kwmissing) > 2 else "") +
                         (" and '%s'" % kwmissing[-1] if len(kwmissing) > 1 else "")))

    # for key, value in env.items():
    #     if key not in newenv:
    #         newenv[key] = value
    return ChainMap(newenv, env)


class Lambda:
    def __init__(self, env={}, node=None):
        self.env = env
        self.body = node.body
        self.fields = dict(ast.iter_fields(node.args))

    def __call__(self, *args, __env__=None, **kwargs):
        return eval_expr(
            getenv(funcname="<lambda>", env=__env__ if __env__ is not None else {}, call_args=args, call_kwargs=kwargs,
                   **self.fields), self.body)

    def __repr__(self):
        ret = []

        for x in self.fields["args"][slice(0, (-(len(self.fields["defaults"]))) or len(self.fields["args"]))]:
            ret.append(x.arg)
        for x in reversed(["{}={}".format(x.arg, str_expr(y)) for x, y in
                           zip(reversed(self.fields["args"]), reversed(self.fields["defaults"]))]):
            ret.append(x)

        if self.fields["vararg"] is not None:
            vararg = "*" + self.fields["vararg"].arg
            ret.append(vararg)

        if self.fields["kwarg"] is not None:
            kwarg = "**" + self.fields["kwarg"].arg
            ret.append(kwarg)

        if self.fields["kwonlyargs"]:
            ret.append("*")
            for p, d in zip(self.fields["kwonlyargs"], self.fields["kw_defaults"]):
                if d is not None:
                    ret.append("{}={}".format(p.arg, str_expr(d)))
                else:
                    ret.append(p.arg)

        return "<lambda " + ", ".join(ret) + ": " + " ... >"

class Function:
    def __init__(self, node: ast.FunctionDef, env: ChainMap):
        self.non_locals = env
        self.body = node.body
        self.returns = node.returns
        self.decorators = node.decorator_list
        self.fields = dict(ast.iter_fields(node.args))

    def __call__(self, *args, **kwargs):
        env = self.non_locals.new_child()
        env = getenv(funcname="<lambda>", env=env, call_args=args, call_kwargs=kwargs, **self.fields)

        for s in self.body:
            if type(s) is ast.Return:
                return eval_expr(env, s.value)
            else:
                try:
                    eval_stmt(env, s)
                except ret_exception as e:
                    return e.args[0]



    def __repr__(self):
        ret = []
        for x in self.fields["args"][slice(0, (-(len(self.fields["defaults"]))) or len(self.fields["args"]))]:
            ret.append(x.arg)
        for x in reversed(["{}={}".format(x.arg, str_expr(y)) for x, y in
                           zip(reversed(self.fields["args"]), reversed(self.fields["defaults"]))]):
            ret.append(x)

        if self.fields["vararg"] is not None:
            vararg = "*" + self.fields["vararg"].arg
            ret.append(vararg)

        if self.fields["kwarg"] is not None:
            kwarg = "**" + self.fields["kwarg"].arg
            ret.append(kwarg)

        if self.fields["kwonlyargs"]:
            ret.append("*")
            for p, d in zip(self.fields["kwonlyargs"], self.fields["kw_defaults"]):
                if d is not None:
                    ret.append("{}={}".format(p.arg, str_expr(d)))
                else:
                    ret.append(p.arg)

        return "<Function definition >" #+ ", ".join(ret) + ": " + ";".join(str_expr(s) for s in self.body) + ">"