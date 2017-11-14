import ast
import unittest

# An id function is useful for testing.
eval_fn = lambda x, _: x
str_fn = lambda x: str(x)
env = {}


class UnaryOpsTest(unittest.TestCase):
    def test_not(self):
        self.assertEqual(unaryops[ast.Not].evaluate(env, ast.NameConstant(value=True)), False)
        self.assertEqual(unaryops[ast.Not].evaluate(env, ast.NameConstant(value=False)), True)

    def test_not_pp(self):
        self.assertEqual(unaryops[ast.Not].pprint(True), "not True")
        self.assertEqual(unaryops[ast.Not].pprint(False), "not False")

    def test_invert(self):
        self.assertEqual(unaryops[ast.Invert].evaluate(env, ast.Num(n=1)), -2)
        self.assertEqual(unaryops[ast.Invert].evaluate(env, ast.Num(n=15)), -16)

    def test_invert_pp(self):
        self.assertEqual(unaryops[ast.Invert].pprint(ast.Num(n=1)), "~1")
        self.assertEqual(unaryops[ast.Invert].pprint(ast.Num(n=15)), "~15")

    def test_uadd(self):
        self.assertEqual(unaryops[ast.UAdd].evaluate(env, ast.Num(n=1)), 1)
        self.assertEqual(unaryops[ast.UAdd].evaluate(env, ast.Num(n=-1)), -1)

    def test_uadd_pp(self):
        self.assertEqual(unaryops[ast.UAdd].pprint(ast.Num(n=1)), "+1")
        self.assertEqual(unaryops[ast.UAdd].pprint(ast.Num(n=-1)), "+-1")

    def test_usub(self):
        self.assertEqual(unaryops[ast.USub].evaluate(env, ast.Num(n=1)), -1)
        self.assertEqual(unaryops[ast.USub].evaluate(env, ast.Num(n=-1)), 1)

    def test_usub_pp(self):
        self.assertEqual(unaryops[ast.USub].pprint(ast.Num(n=1)), "-1")
        self.assertEqual(unaryops[ast.USub].pprint(ast.Num(n=-1)), "--1")
