import unittest
from decimal import Decimal
from milkrate import payout, rate_per_litre, validate_entry
from Task09.calculator import calculate_record

class PaymentTests(unittest.TestCase):
    def test_standard_rate(self):
        self.assertEqual(rate_per_litre(3.5, 8.5), Decimal("30.00"))
    def test_fat_and_snf_above(self):
        self.assertEqual(rate_per_litre(4.2, 8.7), Decimal("33.40"))
        self.assertEqual(payout(8.5, 4.2, 8.7), Decimal("283.90"))
    def test_below(self):
        self.assertEqual(rate_per_litre(3.1, 8.3), Decimal("27.80"))
        self.assertEqual(payout(12, 3.1, 8.3), Decimal("333.60"))
    def test_fat_boundaries(self):
        self.assertTrue(validate_entry("F1", 1, 2.0, 8.5, "M")[0])
        self.assertTrue(validate_entry("F1", 1, 7.0, 8.5, "E")[0])
    def test_negative_quantity_rejected(self):
        self.assertFalse(validate_entry("F1", -1, 3.5, 8.5, "M")[0])
    def test_fat_out_of_range_rejected(self):
        self.assertFalse(validate_entry("F1", 1, 7.1, 8.5, "M")[0])
    def test_bad_text_rejected(self):
        self.assertFalse(validate_entry("F1", "eight", 3.5, 8.5, "M")[0])
    def test_blank_id_rejected(self):
        self.assertFalse(validate_entry("", 1, 3.5, 8.5, "M")[0])
    def test_invalid_shift_rejected(self):
        self.assertFalse(validate_entry("F1", 1, 3.5, 8.5, "night")[0])
    def test_snf_out_of_range_rejected(self):
        self.assertFalse(validate_entry("F1", 1, 3.5, 10.1, "M")[0])
    def test_non_finite_reading_rejected(self):
        self.assertFalse(validate_entry("F1", 1, "NaN", 8.5, "M")[0])
    def test_snf_step_value_parameter(self):
        self.assertEqual(rate_per_litre(3.5, 8.6, 30, 0.4, 0.25), Decimal("30.25"))

if __name__ == "__main__":
    unittest.main()
