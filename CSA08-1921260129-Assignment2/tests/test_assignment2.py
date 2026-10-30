import unittest
from Task01.subsidy import separate_if_decision, elif_decision, overlapping_if_example
from Task01.alternative_matchcase import match_case_decision
from Task02.otp_attempts import verify_while, verify_for, verify_recursive
from Task03.vehicle_number import normalise, is_valid, format_receipt
from Task04.string_building import build_plus, build_join, build_fstring, build_stringio
from Task05.functions_scope import add_item, make_order_adder
from Task06.temple_steps import ways_naive, ways_memo, ways_iterative

class Assignment2Tests(unittest.TestCase):
    def test_subsidy_boundaries(self):
        self.assertEqual(elif_decision(100, False, False), "Full subsidy")
        self.assertEqual(elif_decision(101, True, False), "Partial subsidy")
        self.assertEqual(elif_decision(200, False, False), "No subsidy")
        self.assertEqual(elif_decision(201, False, True), "Senior exception subsidy")

    def test_if_and_elif_agree(self):
        self.assertEqual(separate_if_decision(150, True, False), [elif_decision(150, True, False)])

    def test_overlapping_if_example(self):
        self.assertEqual(len(overlapping_if_example(80, True)), 2)

    def test_match_case(self):
        self.assertEqual(match_case_decision(201, False, True), "Senior exception subsidy")

    def test_otp_blank_does_not_consume_attempt(self):
        self.assertTrue(verify_while(["", "111", "123456"], "123456", 2))
        self.assertTrue(verify_for(["", "111", "123456"], "123456", 2))
        self.assertFalse(verify_for(["", "111", "222", "333"], "123456", 3))

    def test_recursive_otp_alternative(self):
        self.assertTrue(verify_recursive(["", "111", "123456"], "123456", 2))
        self.assertFalse(verify_recursive(["111", "222", "333"], "123456", 3))

    def test_vehicle_normalise(self):
        self.assertEqual(normalise("tn 09 ab 1234"), "TN09AB1234")

    def test_vehicle_valid(self):
        self.assertTrue(is_valid("TN09AB1234"))
        self.assertTrue(is_valid("KA01M0007"))
        self.assertFalse(is_valid("TN9AB1234"))
        self.assertFalse(is_valid("TN221234AB"))

    def test_vehicle_receipt(self):
        self.assertEqual(format_receipt("TN09AB1234"), "TN 09 AB 1234")

    def test_string_builders(self):
        parts=["a", "b", "c"]
        self.assertEqual(build_plus(parts), build_join(parts))
        self.assertEqual(build_join(parts), build_fstring(parts))
        self.assertEqual(build_join(parts), build_stringio(parts))

    def test_independent_orders(self):
        self.assertEqual(add_item("Tea"), ["Tea"])
        self.assertEqual(add_item("Vada"), ["Vada"])

    def test_closure_order_is_private(self):
        add = make_order_adder()
        self.assertEqual(add("Tea"), ["Tea"])
        self.assertEqual(add("Vada"), ["Tea", "Vada"])

    def test_climb_answers(self):
        self.assertEqual([ways_iterative(n) for n in range(1,7)], [1,2,3,5,8,13])
        self.assertEqual(ways_naive(10), ways_memo(10))

if __name__ == "__main__":
    unittest.main()
