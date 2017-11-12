from operations.bind import bind


def generate(gens, env, eval_fn):
    if not gens:
        yield env
    else:
        gen = gens[0]
        for it in eval_fn(gen.iter, env):
            for genenv in generate(gens[1:], bind(gen.target, it, env.copy()), eval_fn):
                if all(eval_fn(if_, genenv) for if_ in gen.ifs):
                    yield genenv


def str_generate(gens, str_fn):
    return " ".join(str_fn(gen.target) + " in " + str_fn(gen.iter) +
                    ((" if " + " ".join(str_fn(IF) for IF in gen.ifs)) if gen.ifs else "") for gen in gens)
