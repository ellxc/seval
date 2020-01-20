import ast
from collections import ChainMap
from seval.constants.blacklist import blacklist
from seval.nodes.evals import eval_stmt
LOOP_LIMIT = 1000

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
    # print(body)
    responses = []
    resp_num = 0
    env = ChainMap()
    env["print"] = lambda *x: [responses.append(y) for y in x] and None
    for stmt_or_expr in body:
        eval_stmt(env, stmt_or_expr, blacklist)
        if resp_num != len(responses):
            for r in responses[resp_num:]:
                print(r)
            resp_num = len(responses)
        # if response is not None:
        # #     print(response)
        #     responses.append(response)


    # return responses, env
