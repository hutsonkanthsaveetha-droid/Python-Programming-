import csv
import tempfile
import unittest
import subprocess
import sys
from pathlib import Path

from TaskA5.ai_app import label, score, summarize, answer_question
from TaskB1.complete_code import load_clean, min_max
from TaskB1.cleaning_pipeline import read_raw_files, clean_records
from TaskB2.adversarial_checks import inspect_file, sql_injection_demo

ROOT = Path(__file__).resolve().parents[1]


class Assignment5Tests(unittest.TestCase):
    def test_complete_code_expected_rows(self):
        from TaskB1.complete_code import RAW
        self.assertEqual(load_clean(RAW), [
            ("Adyar", "2026-10-01", 48.0),
            ("Guindy", "2026-10-01", 95.0),
            ("Guindy", "2026-10-03", 121.0),
        ])

    def test_min_max_expected(self):
        self.assertEqual(min_max([48.0, 95.0, 121.0]), [0.0, 0.644, 1.0])

    def test_min_max_constant_and_empty(self):
        self.assertEqual(min_max([4, 4]), [0.0, 0.0])
        self.assertEqual(min_max([]), [])

    def test_negation_flips_sentiment(self):
        self.assertEqual(label("The staff were not helpful."), "negative")
        self.assertEqual(label("Not bad, service improved."), "positive")

    def test_sentiment_basic(self):
        self.assertEqual(label("The roads are clean and safe."), "positive")
        self.assertEqual(label("The air is dirty and harmful."), "negative")

    def test_summarizer_returns_sentence(self):
        result = summarize("The road is clean. The road is clean and safe. Traffic is slow.", 1)
        self.assertTrue(result.endswith("."))
        self.assertIn("road", result.lower())

    def test_parameterized_sql_is_safe(self):
        unsafe, safe = sql_injection_demo()
        self.assertEqual(len(unsafe), 3)
        self.assertEqual(safe, [])

    def test_adversarial_empty_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "empty.csv"
            path.write_text("", encoding="utf-8")
            self.assertEqual(inspect_file(path), "EMPTY: no records")

    def test_adversarial_semicolon_delimiter(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "semicolon.csv"
            path.write_text("station;date;hour;pm25\nAdyar;2026-10-01;12;48\n", encoding="utf-8")
            self.assertIn("delimiter=';'", inspect_file(path))

    def test_raw_dataset_and_cleaning(self):
        raw, rejected = read_raw_files(ROOT / "data" / "raw")
        cleaned, imputed = clean_records(raw)
        self.assertEqual(len(raw), 8639)
        self.assertEqual(len(cleaned), 8639)
        self.assertEqual(len(rejected), 2)
        self.assertEqual(imputed, 6)
        self.assertTrue(all(r["temperature"] > -50 for r in cleaned))

    def test_chatbot_db(self):
        db = ROOT / "TaskB1" / "outputs" / "air_quality.db"
        if db.exists():
            answer = answer_question("What is the PM2.5 in Adyar today?", db)
            self.assertIn("Adyar", answer)
        else:
            self.skipTest("Run TaskB1 pipeline to create database")

    def test_b2_complete_code_expected_output(self):
        output = subprocess.check_output([sys.executable, "-m", "TaskB2.complete_code"], cwd=ROOT, text=True)
        self.assertIn("54.0 108.0", output)
        self.assertIn("None", output)

    def test_b4_complete_code_expected_labels(self):
        output = subprocess.check_output([sys.executable, "-m", "TaskB4.complete_code"], cwd=ROOT, text=True)
        self.assertIn("positive | Roads are clean and the bus was fast.", output)
        self.assertIn("negative | The staff were not helpful.", output)
        self.assertIn("positive | Not bad, service improved.", output)


if __name__ == "__main__":
    unittest.main()
