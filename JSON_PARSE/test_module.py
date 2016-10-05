from parser import ParseDoc

from filereader import DocProcess
from util import Utility

"""
This is for my unit test. All tests are done in Mac
"""


def test_util(fname):
    lines = Utility.file_len(fname)
    assert lines == 64
    lines, split_list = Utility.split_files(fname, lines, 4)
    assert len(split_list) == 4
    assert lines == 16
    return lines, split_list


def test_file_reader(fname, lines):
    print fname
    dp = DocProcess(fname, lines)
    dp.read_csv()
    for line_no, row in dp.next():
        print line_no, row


def test_parser():
    pd = ParseDoc()
    docs = ['Booker T., Washington, 87360, 373 781 7380, yellow',
            'Chandler, Kerri, (623)-668-9293, pink, 123123121',
            'Ballentine, Hyo, (182)-424-5300, blue, 21351',
            'James Murphy, yellow, 018 154 6474, 83880',
            'James Murphy, yellow, 83880, 018 154 6474',
            'James Murphy,eric, yellow, 8380, 018 154 6474',
            'James Murphy,  83880, 018 154 647',
            'James Murphy, yellow, 83880, 018 154 647',
            'Ballentine, Hyo, (182)-424-5300, blue, 21351']

    for doc in docs:
        valid = pd.parse_machine(doc.split(','))
        print valid

'''
lines, split_list = test_util('/Users/sandipnandi/MYASSN/Assignments/percolate/back_end_rolodex/data.in')
test_file_reader(split_list[2], lines)
test_parser()
test_tinydb()
'''
test_parser()