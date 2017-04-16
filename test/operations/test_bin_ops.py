import ast
import unittest
from operations.bin_ops import BIN_OPS
from operations.expr import str_expr

# An id function is useful for testing.
eval_fn = lambda _, x: x
str_fn = lambda x: str(x)
env = {}

class BinOpsTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(BIN_OPS[ast.Add].evaluate(env, eval_fn, 3, 4), 7)
        self.assertEqual(BIN_OPS[ast.Add].evaluate(env, eval_fn, -3, 4), 1)
        self.assertEqual(BIN_OPS[ast.Add].evaluate(env, eval_fn, -3, -4), -7)
        self.assertAlmostEqual(BIN_OPS[ast.Add].evaluate(env, eval_fn, 1, 3.028), 4.028)

    def test_add_pp(self):
        self.assertEqual(BIN_OPS[ast.Add].pprint(str_fn, 3, 4), "3+4")
        self.assertEqual(BIN_OPS[ast.Add].pprint(str_fn, -3, 4), "-3+4")
        self.assertEqual(BIN_OPS[ast.Add].pprint(str_fn, -3, -4), "-3+-4")
        self.assertEqual(BIN_OPS[ast.Add].pprint(str_fn, 1, 3.028), "1+3.028")

    def test_subtract(self):
        self.assertEqual(BIN_OPS[ast.Sub].evaluate(env, eval_fn, 3, 4), -1)
        self.assertEqual(BIN_OPS[ast.Sub].evaluate(env, eval_fn, -3, 4), -7)
        self.assertEqual(BIN_OPS[ast.Sub].evaluate(env, eval_fn, -3, -4), 1)
        self.assertAlmostEqual(BIN_OPS[ast.Sub].evaluate(env, eval_fn, 1, 3.028), -2.028)

    def test_subtract_pp(self):
        self.assertEqual(BIN_OPS[ast.Sub].pprint(str_fn, 3, 4), "3-4")
        self.assertEqual(BIN_OPS[ast.Sub].pprint(str_fn, -3, 4), "-3-4")
        self.assertEqual(BIN_OPS[ast.Sub].pprint(str_fn, -3, -4), "-3--4")
        self.assertEqual(BIN_OPS[ast.Sub].pprint(str_fn, 1, 3.028), "1-3.028")

    def test_multi(self):
        self.assertEqual(BIN_OPS[ast.Mult].evaluate(env, eval_fn, 3, 4), 12)
        self.assertEqual(BIN_OPS[ast.Mult].evaluate(env, eval_fn, -3, 4), -12)
        self.assertEqual(BIN_OPS[ast.Mult].evaluate(env, eval_fn, -3, -4), 12)
        self.assertAlmostEqual(BIN_OPS[ast.Mult].evaluate(env, eval_fn, 1, 3.028), 3.028)
        self.assertAlmostEqual(BIN_OPS[ast.Mult].evaluate(env, eval_fn, 0.5, 3.028), 1.514)

    def test_multi_pp(self):
        self.assertEqual(BIN_OPS[ast.Mult].pprint(str_fn, 3, 4), "3*4")
        self.assertEqual(BIN_OPS[ast.Mult].pprint(str_fn, -3, 4), "-3*4")
        self.assertEqual(BIN_OPS[ast.Mult].pprint(str_fn, -3, -4), "-3*-4")
        self.assertEqual(BIN_OPS[ast.Mult].pprint(str_fn, 1, 3.028), "1*3.028")
        self.assertEqual(BIN_OPS[ast.Mult].pprint(str_fn, 0.5, 3.028), "0.5*3.028")

    def test_div(self):
        self.assertEqual(BIN_OPS[ast.Div].evaluate(env, eval_fn, 8, 4), 2)
        self.assertEqual(BIN_OPS[ast.Div].evaluate(env, eval_fn, -8, 4), -2)
        self.assertEqual(BIN_OPS[ast.Div].evaluate(env, eval_fn, -8, -4), 2)
        with self.assertRaises(ZeroDivisionError) as _:
            BIN_OPS[ast.Div].evaluate(env, eval_fn, 2, 0)
        self.assertAlmostEqual(BIN_OPS[ast.Div].evaluate(env, eval_fn, 1, 4), 0.25)
        self.assertAlmostEqual(BIN_OPS[ast.Div].evaluate(env, eval_fn, 3.028, 2), 1.514)

    def test_div_pp(self):
        self.assertEqual(BIN_OPS[ast.Div].pprint(str_fn, 8, 4), "8/4")
        self.assertEqual(BIN_OPS[ast.Div].pprint(str_fn, -8, 4), "-8/4")
        self.assertEqual(BIN_OPS[ast.Div].pprint(str_fn, -8, -4), "-8/-4")
        self.assertEqual(BIN_OPS[ast.Div].pprint(str_fn, 1, 4), "1/4")
        self.assertEqual(BIN_OPS[ast.Div].pprint(str_fn, 3.028, 2), "3.028/2")

    def test_mod(self):
        self.assertEqual(BIN_OPS[ast.Mod].evaluate(env, eval_fn, 5, 2), 1)
        self.assertEqual(BIN_OPS[ast.Mod].evaluate(env, eval_fn, 5, 5), 0)
        self.assertEqual(BIN_OPS[ast.Mod].evaluate(env, eval_fn, 5, 3), 2)
        self.assertAlmostEqual(BIN_OPS[ast.Mod].evaluate(env, eval_fn, 5, 3.1415), 1.8585)

    def test_mod_pp(self):
        self.assertEqual(BIN_OPS[ast.Mod].pprint(str_fn, 5, 2), "5%2")
        self.assertEqual(BIN_OPS[ast.Mod].pprint(str_fn, 5, 5), "5%5")
        self.assertEqual(BIN_OPS[ast.Mod].pprint(str_fn, 5, 3), "5%3")
        self.assertEqual(BIN_OPS[ast.Mod].pprint(str_fn, 5, 3.1415), "5%3.1415")

    def test_pow(self):
        self.assertEqual(BIN_OPS[ast.Pow].evaluate(env, eval_fn, 5, 2), 25)
        self.assertEqual(BIN_OPS[ast.Pow].evaluate(env, eval_fn, 5, 4), 625)
        self.assertEqual(BIN_OPS[ast.Pow].evaluate(env, eval_fn, 5, 0), 1)
        self.assertAlmostEqual(BIN_OPS[ast.Pow].evaluate(env, eval_fn, 5, -1), 0.2)
        self.assertAlmostEqual(BIN_OPS[ast.Pow].evaluate(env, eval_fn, 25, 0.5), 5.0)

    def test_pow_pp(self):
        self.assertEqual(BIN_OPS[ast.Pow].pprint(str_fn, 5, 2), "5**2")
        self.assertEqual(BIN_OPS[ast.Pow].pprint(str_fn, 5, 4), "5**4")
        self.assertEqual(BIN_OPS[ast.Pow].pprint(str_fn, 5, 0), "5**0")
        self.assertEqual(BIN_OPS[ast.Pow].pprint(str_fn, 5, -1), "5**-1")
        self.assertEqual(BIN_OPS[ast.Pow].pprint(str_fn, 25, 0.5), "25**0.5")

    def test_lshift(self):
        self.assertEqual(BIN_OPS[ast.LShift].evaluate(env, eval_fn, 2, 3), 16)
        with self.assertRaises(ValueError) as _:
            BIN_OPS[ast.LShift].evaluate(env, eval_fn, 2, -1)
        self.assertEqual(BIN_OPS[ast.LShift].evaluate(env, eval_fn, 3, 2), 0b1100)

    def test_lshift_pp(self):
        self.assertEqual(BIN_OPS[ast.LShift].pprint(str_fn, 2, 3), "2<<3")
        self.assertEqual(BIN_OPS[ast.LShift].pprint(str_fn, 3, 2), "3<<2")

    def test_rshift(self):
        self.assertEqual(BIN_OPS[ast.RShift].evaluate(env, eval_fn, 2, 1), 1)
        self.assertEqual(BIN_OPS[ast.RShift].evaluate(env, eval_fn, 16, 3), 2)
        with self.assertRaises(ValueError) as _:
            BIN_OPS[ast.RShift].evaluate(env, eval_fn, 2, -1)
        self.assertEqual(BIN_OPS[ast.RShift].evaluate(env, eval_fn, 3, 2), 0)

    def test_rshift_pp(self):
        self.assertEqual(BIN_OPS[ast.RShift].pprint(str_fn, 2, 1), "2>>1")
        self.assertEqual(BIN_OPS[ast.RShift].pprint(str_fn, 16, 3), "16>>3")
        self.assertEqual(BIN_OPS[ast.RShift].pprint(str_fn, 3, 2), "3>>2")

    def test_bit_or(self):
        self.assertEqual(BIN_OPS[ast.BitOr].evaluate(env, eval_fn, 7, 3), 7)
        self.assertEqual(BIN_OPS[ast.BitOr].evaluate(env, eval_fn, 8, 3), 11)
        self.assertEqual(BIN_OPS[ast.BitOr].evaluate(env, eval_fn, 9, 3), 11)
        self.assertEqual(BIN_OPS[ast.BitOr].evaluate(env, eval_fn, 16, -1), -1)
        with self.assertRaises(TypeError) as _:
            BIN_OPS[ast.BitAnd].evaluate(env, eval_fn, 2.3, 1)

    def test_bit_or_pp(self):
        self.assertEqual(BIN_OPS[ast.BitOr].pprint(str_fn, 7, 3), "7|3")
        self.assertEqual(BIN_OPS[ast.BitOr].pprint(str_fn, 8, 3), "8|3")
        self.assertEqual(BIN_OPS[ast.BitOr].pprint(str_fn, 9, 3), "9|3")
        self.assertEqual(BIN_OPS[ast.BitOr].pprint(str_fn, 16, -1), "16|-1")

    def test_bit_xor(self):
        self.assertEqual(BIN_OPS[ast.BitXor].evaluate(env, eval_fn, 7, 3), 4)
        self.assertEqual(BIN_OPS[ast.BitXor].evaluate(env, eval_fn, 8, 3), 11)
        self.assertEqual(BIN_OPS[ast.BitXor].evaluate(env, eval_fn, 9, 3), 10)
        self.assertEqual(BIN_OPS[ast.BitXor].evaluate(env, eval_fn, 16, -1), -17)
        with self.assertRaises(TypeError) as _:
            BIN_OPS[ast.BitAnd].evaluate(env, eval_fn, 2.3, 1)

    def test_bit_xor_pp(self):
        self.assertEqual(BIN_OPS[ast.BitXor].pprint(str_fn, 7, 3), "7^3")
        self.assertEqual(BIN_OPS[ast.BitXor].pprint(str_fn, 8, 3), "8^3")
        self.assertEqual(BIN_OPS[ast.BitXor].pprint(str_fn, 9, 3), "9^3")
        self.assertEqual(BIN_OPS[ast.BitXor].pprint(str_fn, 16, -1), "16^-1")

    def test_bit_and(self):
        self.assertEqual(BIN_OPS[ast.BitAnd].evaluate(env, eval_fn, 7, 3), 3)
        self.assertEqual(BIN_OPS[ast.BitAnd].evaluate(env, eval_fn, 8, 3), 0)
        self.assertEqual(BIN_OPS[ast.BitAnd].evaluate(env, eval_fn, 9, 3), 1)
        self.assertEqual(BIN_OPS[ast.BitAnd].evaluate(env, eval_fn, 16, -1), 16)
        with self.assertRaises(TypeError) as _:
            BIN_OPS[ast.BitAnd].evaluate(env, eval_fn, 2.3, 1)

    def test_bit_and_pp(self):
        self.assertEqual(BIN_OPS[ast.BitAnd].pprint(str_fn, 7, 3), "7&3")
        self.assertEqual(BIN_OPS[ast.BitAnd].pprint(str_fn, 8, 3), "8&3")
        self.assertEqual(BIN_OPS[ast.BitAnd].pprint(str_fn, 9, 3), "9&3")
        self.assertEqual(BIN_OPS[ast.BitAnd].pprint(str_fn, 16, -1), "16&-1")

    def test_floor_div(self):
        self.assertEqual(BIN_OPS[ast.FloorDiv].evaluate(env, eval_fn, 8, 4), 2)
        self.assertEqual(BIN_OPS[ast.FloorDiv].evaluate(env, eval_fn, 7, 4), 1)
        self.assertEqual(BIN_OPS[ast.FloorDiv].evaluate(env, eval_fn, -8, 4), -2)
        self.assertEqual(BIN_OPS[ast.FloorDiv].evaluate(env, eval_fn, -8, -4), 2)
        with self.assertRaises(ZeroDivisionError) as _:
            BIN_OPS[ast.FloorDiv].evaluate(env, eval_fn, 2, 0)
        self.assertEqual(BIN_OPS[ast.FloorDiv].evaluate(env, eval_fn, 1, 4), 0)
        self.assertEqual(BIN_OPS[ast.FloorDiv].evaluate(env, eval_fn, 3.028, 2), 1)

    def test_floor_div_pp(self):
        self.assertEqual(BIN_OPS[ast.FloorDiv].pprint(str_fn, 8, 4), "8//4")
        self.assertEqual(BIN_OPS[ast.FloorDiv].pprint(str_fn, 7, 4), "7//4")
        self.assertEqual(BIN_OPS[ast.FloorDiv].pprint(str_fn, -8, 4), "-8//4")
        self.assertEqual(BIN_OPS[ast.FloorDiv].pprint(str_fn, -8, -4), "-8//-4")
        self.assertEqual(BIN_OPS[ast.FloorDiv].pprint(str_fn, 1, 4), "1//4")
        self.assertEqual(BIN_OPS[ast.FloorDiv].pprint(str_fn, 3.028, 2), "3.028//2")