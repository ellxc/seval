import ast
import unittest

from nodes.operator import operators

# An id function is useful for testing.
env = {}


class BinOpsTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(operators[ast.Add].evaluate(env, ast.Num(n=3), ast.Num(n=4)), 7)
        self.assertEqual(operators[ast.Add].evaluate(env, ast.Num(n=-3), ast.Num(n=4)), 1)
        self.assertEqual(operators[ast.Add].evaluate(env, ast.Num(n=-3), ast.Num(n=-4)), -7)
        self.assertAlmostEqual(operators[ast.Add].evaluate(env, ast.Num(n=1), ast.Num(n=3.028)), 4.028)

    def test_add_pp(self):
        self.assertEqual(operators[ast.Add].pprint(ast.Num(n=3), ast.Num(n=4)), "3+4")
        self.assertEqual(operators[ast.Add].pprint(ast.Num(n=-3), ast.Num(n=4)), "-3+4")
        self.assertEqual(operators[ast.Add].pprint(ast.Num(n=-3), ast.Num(n=-4)), "-3+-4")
        self.assertEqual(operators[ast.Add].pprint(ast.Num(n=1), ast.Num(n=3.028)), "1+3.028")

    def test_subtract(self):
        self.assertEqual(operators[ast.Sub].evaluate(env, ast.Num(n=3), ast.Num(n=4)), -1)
        self.assertEqual(operators[ast.Sub].evaluate(env, ast.Num(n=-3), ast.Num(n=4)), -7)
        self.assertEqual(operators[ast.Sub].evaluate(env, ast.Num(n=-3), ast.Num(n=-4)), 1)
        self.assertAlmostEqual(operators[ast.Sub].evaluate(env, ast.Num(n=1), ast.Num(n=3.028)), -2.028)

    def test_subtract_pp(self):
        self.assertEqual(operators[ast.Sub].pprint(ast.Num(n=3), ast.Num(n=4)), "3-4")
        self.assertEqual(operators[ast.Sub].pprint(ast.Num(n=-3), ast.Num(n=4)), "-3-4")
        self.assertEqual(operators[ast.Sub].pprint(ast.Num(n=-3), ast.Num(n=-4)), "-3--4")
        self.assertEqual(operators[ast.Sub].pprint(ast.Num(n=1), ast.Num(n=3.028)), "1-3.028")

    def test_multi(self):
        self.assertEqual(operators[ast.Mult].evaluate(env, ast.Num(n=3), ast.Num(n=4)), 12)
        self.assertEqual(operators[ast.Mult].evaluate(env, ast.Num(n=-3), ast.Num(n=4)), -12)
        self.assertEqual(operators[ast.Mult].evaluate(env, ast.Num(n=-3), ast.Num(n=-4)), 12)
        self.assertAlmostEqual(operators[ast.Mult].evaluate(env, ast.Num(n=1), ast.Num(n=3.028)), 3.028)
        self.assertAlmostEqual(operators[ast.Mult].evaluate(env, ast.Num(n=0.5), ast.Num(n=3.028)), 1.514)

    def test_multi_pp(self):
        self.assertEqual(operators[ast.Mult].pprint(ast.Num(n=3), ast.Num(n=4)), "3*4")
        self.assertEqual(operators[ast.Mult].pprint(ast.Num(n=-3), ast.Num(n=4)), "-3*4")
        self.assertEqual(operators[ast.Mult].pprint(ast.Num(n=-3), ast.Num(n=-4)), "-3*-4")
        self.assertEqual(operators[ast.Mult].pprint(ast.Num(n=1), ast.Num(n=3.028)), "1*3.028")
        self.assertEqual(operators[ast.Mult].pprint(ast.Num(n=0.5), ast.Num(n=3.028)), "0.5*3.028")

    def test_div(self):
        self.assertEqual(operators[ast.Div].evaluate(env, ast.Num(n=8), ast.Num(n=4)), 2)
        self.assertEqual(operators[ast.Div].evaluate(env, ast.Num(n=-8), ast.Num(n=4)), -2)
        self.assertEqual(operators[ast.Div].evaluate(env, ast.Num(n=-8), ast.Num(n=-4)), 2)
        with self.assertRaises(ZeroDivisionError) as _:
            operators[ast.Div].evaluate(env, ast.Num(n=2), ast.Num(n=0))
        self.assertAlmostEqual(operators[ast.Div].evaluate(env, ast.Num(n=1), ast.Num(n=4)), 0.25)
        self.assertAlmostEqual(operators[ast.Div].evaluate(env, ast.Num(n=3.028), ast.Num(n=2)), 1.514)

    def test_div_pp(self):
        self.assertEqual(operators[ast.Div].pprint(ast.Num(n=8), ast.Num(n=4)), "8/4")
        self.assertEqual(operators[ast.Div].pprint(ast.Num(n=-8), ast.Num(n=4)), "-8/4")
        self.assertEqual(operators[ast.Div].pprint(ast.Num(n=-8), ast.Num(n=-4)), "-8/-4")
        self.assertEqual(operators[ast.Div].pprint(ast.Num(n=1), ast.Num(n=4)), "1/4")
        self.assertEqual(operators[ast.Div].pprint(ast.Num(n=3.028), ast.Num(n=2)), "3.028/2")

    def test_mod(self):
        self.assertEqual(operators[ast.Mod].evaluate(env, ast.Num(n=5), ast.Num(n=2)), 1)
        self.assertEqual(operators[ast.Mod].evaluate(env, ast.Num(n=5), ast.Num(n=5)), 0)
        self.assertEqual(operators[ast.Mod].evaluate(env, ast.Num(n=5), ast.Num(n=3)), 2)
        self.assertAlmostEqual(operators[ast.Mod].evaluate(env, ast.Num(n=5), ast.Num(n=3.1415)), 1.8585)

    def test_mod_pp(self):
        self.assertEqual(operators[ast.Mod].pprint(ast.Num(n=5), ast.Num(n=2)), "5%2")
        self.assertEqual(operators[ast.Mod].pprint(ast.Num(n=5), ast.Num(n=5)), "5%5")
        self.assertEqual(operators[ast.Mod].pprint(ast.Num(n=5), ast.Num(n=3)), "5%3")
        self.assertEqual(operators[ast.Mod].pprint(ast.Num(n=5), ast.Num(n=3.1415)), "5%3.1415")

    def test_pow(self):
        self.assertEqual(operators[ast.Pow].evaluate(env, ast.Num(n=5), ast.Num(n=2)), 25)
        self.assertEqual(operators[ast.Pow].evaluate(env, ast.Num(n=5), ast.Num(n=4)), 625)
        self.assertEqual(operators[ast.Pow].evaluate(env, ast.Num(n=5), ast.Num(n=0)), 1)
        self.assertAlmostEqual(operators[ast.Pow].evaluate(env, ast.Num(n=5), ast.Num(n=-1)), 0.2)
        self.assertAlmostEqual(operators[ast.Pow].evaluate(env, ast.Num(n=25), ast.Num(n=0.5)), 5.0)

    def test_pow_pp(self):
        self.assertEqual(operators[ast.Pow].pprint(ast.Num(n=5), ast.Num(n=2)), "5**2")
        self.assertEqual(operators[ast.Pow].pprint(ast.Num(n=5), ast.Num(n=4)), "5**4")
        self.assertEqual(operators[ast.Pow].pprint(ast.Num(n=5), ast.Num(n=0)), "5**0")
        self.assertEqual(operators[ast.Pow].pprint(ast.Num(n=5), ast.Num(n=-1)), "5**-1")
        self.assertEqual(operators[ast.Pow].pprint(ast.Num(n=25), ast.Num(n=0.5)), "25**0.5")

    def test_lshift(self):
        self.assertEqual(operators[ast.LShift].evaluate(env, ast.Num(n=2), ast.Num(n=3)), 16)
        with self.assertRaises(ValueError) as _:
            operators[ast.LShift].evaluate(env, ast.Num(n=2), ast.Num(n=-1))
        self.assertEqual(operators[ast.LShift].evaluate(env, ast.Num(n=3), ast.Num(n=2)), 0b1100)

    def test_lshift_pp(self):
        self.assertEqual(operators[ast.LShift].pprint(ast.Num(n=2), ast.Num(n=3)), "2<<3")
        self.assertEqual(operators[ast.LShift].pprint(ast.Num(n=3), ast.Num(n=2)), "3<<2")

    def test_rshift(self):
        self.assertEqual(operators[ast.RShift].evaluate(env, ast.Num(n=2), ast.Num(n=1)), 1)
        self.assertEqual(operators[ast.RShift].evaluate(env, ast.Num(n=16), ast.Num(n=3)), 2)
        with self.assertRaises(ValueError) as _:
            operators[ast.RShift].evaluate(env, ast.Num(n=2), ast.Num(n=-1))
        self.assertEqual(operators[ast.RShift].evaluate(env, ast.Num(n=3), ast.Num(n=2)), 0)

    def test_rshift_pp(self):
        self.assertEqual(operators[ast.RShift].pprint(ast.Num(n=2), ast.Num(n=1)), "2>>1")
        self.assertEqual(operators[ast.RShift].pprint(ast.Num(n=16), ast.Num(n=3)), "16>>3")
        self.assertEqual(operators[ast.RShift].pprint(ast.Num(n=3), ast.Num(n=2)), "3>>2")

    def test_bit_or(self):
        self.assertEqual(operators[ast.BitOr].evaluate(env, ast.Num(n=7), ast.Num(n=3)), 7)
        self.assertEqual(operators[ast.BitOr].evaluate(env, ast.Num(n=8), ast.Num(n=3)), 11)
        self.assertEqual(operators[ast.BitOr].evaluate(env, ast.Num(n=9), ast.Num(n=3)), 11)
        self.assertEqual(operators[ast.BitOr].evaluate(env, ast.Num(n=16), ast.Num(n=-1)), -1)
        with self.assertRaises(TypeError) as _:
            operators[ast.BitAnd].evaluate(env, ast.Num(n=2.3), ast.Num(n=1))

    def test_bit_or_pp(self):
        self.assertEqual(operators[ast.BitOr].pprint(ast.Num(n=7), ast.Num(n=3)), "7|3")
        self.assertEqual(operators[ast.BitOr].pprint(ast.Num(n=8), ast.Num(n=3)), "8|3")
        self.assertEqual(operators[ast.BitOr].pprint(ast.Num(n=9), ast.Num(n=3)), "9|3")
        self.assertEqual(operators[ast.BitOr].pprint(ast.Num(n=16), ast.Num(n=-1)), "16|-1")

    def test_bit_xor(self):
        self.assertEqual(operators[ast.BitXor].evaluate(env, ast.Num(n=7), ast.Num(n=3)), 4)
        self.assertEqual(operators[ast.BitXor].evaluate(env, ast.Num(n=8), ast.Num(n=3)), 11)
        self.assertEqual(operators[ast.BitXor].evaluate(env, ast.Num(n=9), ast.Num(n=3)), 10)
        self.assertEqual(operators[ast.BitXor].evaluate(env, ast.Num(n=16), ast.Num(n=-1)), -17)
        with self.assertRaises(TypeError) as _:
            operators[ast.BitAnd].evaluate(env, ast.Num(n=2.3), ast.Num(n=1))

    def test_bit_xor_pp(self):
        self.assertEqual(operators[ast.BitXor].pprint(ast.Num(n=7), ast.Num(n=3)), "7^3")
        self.assertEqual(operators[ast.BitXor].pprint(ast.Num(n=8), ast.Num(n=3)), "8^3")
        self.assertEqual(operators[ast.BitXor].pprint(ast.Num(n=9), ast.Num(n=3)), "9^3")
        self.assertEqual(operators[ast.BitXor].pprint(ast.Num(n=16), ast.Num(n=-1)), "16^-1")

    def test_bit_and(self):
        self.assertEqual(operators[ast.BitAnd].evaluate(env, ast.Num(n=7), ast.Num(n=3)), 3)
        self.assertEqual(operators[ast.BitAnd].evaluate(env, ast.Num(n=8), ast.Num(n=3)), 0)
        self.assertEqual(operators[ast.BitAnd].evaluate(env, ast.Num(n=9), ast.Num(n=3)), 1)
        self.assertEqual(operators[ast.BitAnd].evaluate(env, ast.Num(n=16), ast.Num(n=-1)), 16)
        with self.assertRaises(TypeError) as _:
            operators[ast.BitAnd].evaluate(env, ast.Num(n=2.3), ast.Num(n=1))

    def test_bit_and_pp(self):
        self.assertEqual(operators[ast.BitAnd].pprint(ast.Num(n=7), ast.Num(n=3)), "7&3")
        self.assertEqual(operators[ast.BitAnd].pprint(ast.Num(n=8), ast.Num(n=3)), "8&3")
        self.assertEqual(operators[ast.BitAnd].pprint(ast.Num(n=9), ast.Num(n=3)), "9&3")
        self.assertEqual(operators[ast.BitAnd].pprint(ast.Num(n=16), ast.Num(n=-1)), "16&-1")

    def test_floor_div(self):
        self.assertEqual(operators[ast.FloorDiv].evaluate(env, ast.Num(n=8), ast.Num(n=4)), 2)
        self.assertEqual(operators[ast.FloorDiv].evaluate(env, ast.Num(n=7), ast.Num(n=4)), 1)
        self.assertEqual(operators[ast.FloorDiv].evaluate(env, ast.Num(n=-8), ast.Num(n=4)), -2)
        self.assertEqual(operators[ast.FloorDiv].evaluate(env, ast.Num(n=-8), ast.Num(n=-4)), 2)
        with self.assertRaises(ZeroDivisionError) as _:
            operators[ast.FloorDiv].evaluate(env, ast.Num(n=2), ast.Num(n=0))
        self.assertEqual(operators[ast.FloorDiv].evaluate(env, ast.Num(n=1), ast.Num(n=4)), 0)
        self.assertEqual(operators[ast.FloorDiv].evaluate(env, ast.Num(n=3.028), ast.Num(n=2)), 1)

    def test_floor_div_pp(self):
        self.assertEqual(operators[ast.FloorDiv].pprint(ast.Num(n=8), ast.Num(n=4)), "8//4")
        self.assertEqual(operators[ast.FloorDiv].pprint(ast.Num(n=7), ast.Num(n=4)), "7//4")
        self.assertEqual(operators[ast.FloorDiv].pprint(ast.Num(n=-8), ast.Num(n=4)), "-8//4")
        self.assertEqual(operators[ast.FloorDiv].pprint(ast.Num(n=-8), ast.Num(n=-4)), "-8//-4")
        self.assertEqual(operators[ast.FloorDiv].pprint(ast.Num(n=1), ast.Num(n=4)), "1//4")
        self.assertEqual(operators[ast.FloorDiv].pprint(ast.Num(n=3.028), ast.Num(n=2)), "3.028//2")
