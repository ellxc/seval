import ast

from seval.constants.blacklist import blacklist
from seval.nodes.evals import eval_stmt

def parse_string(env, text):
    body = ast.parse(text, mode='single').body
    responses = []
    for stmt_or_expr in body:
        response = eval_stmt(env, stmt_or_expr, blacklist)
        if response is not None:
            responses.append(response)
    return responses, env


def parse_file(file):
    f = open(file, "r")
    fr = f.read()
    body = ast.parse(fr, mode='exec').body
    print(body)
    # responses = []
    env = {}
    for stmt_or_expr in body:
        response = eval_stmt(env, stmt_or_expr, blacklist)
        if response is not None:
            print(response)
            # responses.append(response)

    # return responses, env
