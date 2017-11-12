from collections import OrderedDict

from operations.bind import bind


def getenv(funcname, args, vararg, kwarg, defaults, call_args, call_kwargs,
           env, eval, kwonlyargs=None, kw_defaults=None):
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
            bind(param, eval(default, env), newenv)
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

    for key, value in env.items():
        if key not in newenv:
            newenv[key] = value
    return newenv


class Lambda():
    def __init__(self, body, fields, eval_fn, str_fun):
        self.body = body
        self.fields = fields
        self.eval = eval_fn
        self.str_fun = str_fun

    def __call__(self, *args, __env__=None, **kwargs):
        if __env__ is None:
            __env__ = dict()
        return self.eval(self.body,
                         getenv(funcname="<lambda>", env=__env__, call_args=args, call_kwargs=kwargs, eval=self.eval,
                                **self.fields))

    def __repr__(self):
        ret = []

        for x in self.fields["args"][slice(0, (-(len(self.fields["defaults"]))) or len(self.fields["args"]))]:
            ret.append(x.arg)
        for x in reversed(["{}={}".format(x.arg, self.str_fun(y)) for x, y in
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
                    ret.append("{}={}".format(p.arg, self.str_fun(d)))
                else:
                    ret.append(p.arg)

        return "<lambda " + ", ".join(ret) + ": " + self.str_fun(self.body) + ">"
