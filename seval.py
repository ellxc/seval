import ast

from operations.assign import eval_assign, eval_augassign, eval_del
from operations.expr import eval_expr


def parse_string(text, env):
    body = ast.parse(text, mode='single').body
    responses = []
    for stmt_or_expr in body:
        response = None
        if isinstance(stmt_or_expr, ast.Expr):
            response = eval_expr(stmt_or_expr.value, env)
        elif isinstance(stmt_or_expr, ast.Assign):
            eval_assign(stmt_or_expr, env)
        elif isinstance(stmt_or_expr, ast.AugAssign):
            eval_augassign(stmt_or_expr, env)
        elif isinstance(stmt_or_expr, ast.Delete):
            eval_del(stmt_or_expr, env)

        if response is not None:
            responses.append(response)
    return responses, env


def parse_file(self, file, mode='exec'):
    pass
