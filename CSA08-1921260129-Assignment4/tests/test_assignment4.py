import csv
import tempfile
import unittest
from pathlib import Path
from decimal import Decimal
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'Task01'))
sys.path.insert(0, str(ROOT / 'Task02'))
sys.path.insert(0, str(ROOT / 'Task03'))
sys.path.insert(0, str(ROOT / 'Task04'))
sys.path.insert(0, str(ROOT / 'Task06'))

from repair_mess import process_mess_file
from attendance_processor import process_month
from attendance_errors import parse_line, summarise, InvalidRecord, AttendanceFileError
from library_returns import process
from fest import process_departments


class Assignment4Tests(unittest.TestCase):
    def test_mess_decimal_total_and_rejects(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'mess.csv'
            p.write_text('1,Asha,1250.50\n2,Ravi,bad\n', encoding='utf-8')
            rows, total, rejected = process_mess_file(p)
            self.assertEqual(total, Decimal('1250.50'))
            self.assertEqual(len(rows), 1)
            self.assertEqual(len(rejected), 1)

    def test_attendance_month_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp, out = Path(tmp) / 'in', Path(tmp) / 'out'
            inp.mkdir()
            (inp / 'd.csv').write_text('1,2026-10-01,P\n1,2026-10-02,A\n2,2026-10-02,X\n', encoding='utf-8')
            counts, bad, paths = process_month(inp, out)
            self.assertEqual(counts['1'], [1, 1])
            self.assertEqual(len(bad), 1)
            self.assertTrue(paths[0].exists())

    def test_parse_line_valid_and_invalid(self):
        self.assertEqual(parse_line('1,2026-10-01,P'), ('1', '2026-10-01', 'P'))
        with self.assertRaises(InvalidRecord):
            parse_line('1,2026-10-01,X')

    def test_summarise_expected_tuple(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'day.csv'
            p.write_text('1,2026-10-01,P\n2,2026-10-01,A\n3,2026-10-01\n', encoding='utf-8')
            self.assertEqual(summarise(p), (1, 1, [(3, 'expected 3 fields, found 2')]))

    def test_summarise_missing_raises_wrapped(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(AttendanceFileError) as cm:
                summarise(Path(tmp) / 'absent.csv')
            self.assertIsInstance(cm.exception.__cause__, FileNotFoundError)

    def test_returns_append(self):
        with tempfile.TemporaryDirectory() as tmp:
            day = Path(tmp) / 'day.txt'
            log = Path(tmp) / 'returns.log'
            day.write_text('Book A\nBook B\n', encoding='utf-8')
            self.assertTrue(process(day, log))
            self.assertTrue(process(day, log))
            self.assertEqual(log.read_text(encoding='utf-8').splitlines(), ['Book A', 'Book B', 'Book A', 'Book B'])

    def test_fest_merge_and_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp, out = Path(tmp) / 'in', Path(tmp) / 'out'
            inp.mkdir()
            (inp / 'CSE.csv').write_text('1,A,CSE,a@example.com,Music\n', encoding='utf-8')
            (inp / 'ECE.csv').write_text('1,A,CSE,b@example.com,Drama\n2,B,ECE,bad,Quiz\n', encoding='utf-8')
            contacts, errors, metrics = process_departments(inp, out, ['CSE', 'ECE', 'EEE'])
            self.assertEqual(len(contacts), 1)
            self.assertEqual(contacts['1']['events'], {'Music', 'Drama'})
            self.assertEqual(metrics['duplicate_lines'], 1)
            self.assertEqual(len(errors), 2)
            self.assertTrue((out / 'clean_master.csv').exists())


if __name__ == '__main__':
    unittest.main()
