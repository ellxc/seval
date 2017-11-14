import ast
import unittest

from operations.unaryop import UNARY_OPS

# An id function is useful for testing.
eval_fn = lambda x, _: x
str_fn = lambda x: str(x)
env = {}


class UnaryOpsTest(unittest.TestCase):
    def test_not(self):
        self.assertEqual(UNARY_OPS[ast.Not].evaluate(env, eval_fn, True), False)
        self.assertEqual(UNARY_OPS[ast.Not].evaluate(env, eval_fn, False), True)

    def test_not_pp(self):
        self.assertEqual(UNARY_OPS[ast.Not].pprint(str_fn, True), "not True")
        self.assertEqual(UNARY_OPS[ast.Not].pprint(str_fn, False), "not False")

    def test_invert(self):
        self.assertEqual(UNARY_OPS[ast.Invert].evaluate(env, eval_fn, 1), -2)
        self.assertEqual(UNARY_OPS[ast.Invert].evaluate(env, eval_fn, 15), -16)

    def test_invert_pp(self):
        self.assertEqual(UNARY_OPS[ast.Invert].pprint(str_fn, 1), "~1")
        self.assertEqual(UNARY_OPS[ast.Invert].pprint(str_fn, 15), "~15")

    def test_uadd(self):
        self.assertEqual(UNARY_OPS[ast.UAdd].evaluate(env, eval_fn, 1), 1)
        self.assertEqual(UNARY_OPS[ast.UAdd].evaluate(env, eval_fn, -1), -1)

    def test_uadd_pp(self):
        self.assertEqual(UNARY_OPS[ast.UAdd].pprint(str_fn, 1), "+1")
        self.assertEqual(UNARY_OPS[ast.UAdd].pprint(str_fn, -1), "+-1")

    def test_usub(self):
        self.assertEqual(UNARY_OPS[ast.USub].evaluate(env, eval_fn, 1), -1)
        self.assertEqual(UNARY_OPS[ast.USub].evaluate(env, eval_fn, -1), 1)

    def test_usub_pp(self):
        self.assertEqual(UNARY_OPS[ast.USub].pprint(str_fn, 1), "-1")
        self.assertEqual(UNARY_OPS[ast.USub].pprint(str_fn, -1), "--1")
