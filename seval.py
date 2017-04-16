import ast
import operations.expr

class Seval:
    def __init__(self):
        pass

    def parse_string(self, text, env):
        body = ast.parse(text, mode='single').body
        responses = []
        response = None
        for stmt_or_expr in body:
            response = None
            if isinstance(stmt_or_expr, ast.Expr):
                response = operations.expr.eval_expr(env, stmt_or_expr.value)
        if response is not None:
            responses.append(response)
        return responses, env


    def parse_file(self, file, mode='exec'):
        pass
