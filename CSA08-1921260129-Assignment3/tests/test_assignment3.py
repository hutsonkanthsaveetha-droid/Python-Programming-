import unittest
from Task01.rainfall import moving_average_naive, moving_average_running, weekly_totals
from Task02.tuples_mutability import change_first
from Task03.complaints import frequencies_get, frequencies_setdefault, top, group_by
from Task04.electives import reports, reports_methods
from Task05.sensor_cleaning import clean_loop, clean_comprehension, clean_map_filter, alarm_minutes
from Task06.timetable import TIMETABLE, build_station_index, find_trains, query_index
from Task07.contact_merge import merge_contacts, normalise_number

class Assignment3Tests(unittest.TestCase):
    def test_q1_moving_average_same(self):
        data=[1,2,3,4,5,6,7,8]
        self.assertEqual(moving_average_naive(data), moving_average_running(data))
    def test_q1_short_and_empty(self):
        self.assertEqual(moving_average_running([]), [])
        self.assertEqual(moving_average_naive([1,2,3]), [])
    def test_q1_weekly_partial(self):
        self.assertEqual(weekly_totals([1,2,3,4,5,6,7,8]), [28,8])
    def test_q2_grid_separate_rows(self):
        grid=[[0 for _ in range(4)] for _ in range(3)]
        grid[0][1]=7
        self.assertEqual(grid[1][1],0)
        self.assertIsNot(grid[0],grid[1])
    def test_q2_tuple_key(self):
        self.assertEqual({(1,2):'x'}[(1,2)],'x')
    def test_q3_frequencies(self):
        texts=['seeds not received seeds delayed','fertiliser price high','seeds price high subsidy not received']
        expected={'seeds':3,'received':2,'delayed':1,'fertiliser':1,'price':2,'subsidy':1}
        self.assertEqual(frequencies_get(texts,{'not','high'}),expected)
        self.assertEqual(frequencies_setdefault(texts,{'not','high'}),expected)
    def test_q3_top_tie_order(self):
        self.assertEqual(top({'received':2,'price':2,'seeds':3},3), [('seeds',3),('price',2),('received',2)])
    def test_q3_group(self):
        records=[{'district':'X','complaint':'one'},{'district':'X','complaint':'two'}]
        self.assertEqual(group_by(records,'district'),{'X':['one','two']})
    def test_q3_punctuation_separates_words(self):
        self.assertEqual(frequencies_get(['seeds,water!'],set()), {'seeds':1,'water':1})
    def test_q4_operators_methods(self):
        a={1,2}; b={2,3}; all_values={1,2,3,4}
        self.assertEqual(reports(a,b,all_values),reports_methods(a,b,all_values))
        self.assertEqual(reports(a,b,all_values),({2},{1,3},{4}))
    def test_q4_empty_and_identical(self):
        all_values={1,2,3}
        self.assertEqual(reports(set(),set(),all_values),(set(),set(),all_values))
        self.assertEqual(reports({1,2},{1,2},all_values),({1,2},set(),{3}))
    def test_q5_methods_same(self):
        data=[-51,-50,0,3,9,51]
        self.assertEqual(clean_loop(data),clean_comprehension(data))
        self.assertEqual(clean_loop(data),clean_map_filter(data))
    def test_q5_alarms(self):
        self.assertEqual(alarm_minutes([4,9,1,51]),[2,3])
    def test_q6_index_same(self):
        idx=build_station_index(TIMETABLE)
        self.assertEqual(find_trains(TIMETABLE,'Katpadi','Tue'),query_index(idx,'Katpadi','Tue'))
    def test_q7_normalise_number(self):
        self.assertEqual(normalise_number('+91 98400 12345'),'9840012345')
    def test_q7_merge(self):
        data={'a':[{'name':'Dr Ravi','phones':['+91 98400 12345'],'emails':[]}],
              'b':[{'name':'Ravi Kumar','phones':['9840012345'],'emails':['r@example.com']}]}
        out=merge_contacts(data)
        self.assertEqual(len(out),1)
        self.assertEqual(out[0]['phones'],{'9840012345'})

if __name__=='__main__': unittest.main()
