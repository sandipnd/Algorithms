import string
import logging
from util import FileNotFound


class DocProcess(object):

    def __init__(self, filename, lines_to_be):
        self.df = None
        self.filename = filename
        self.lines_to_be = lines_to_be
        self.start = 0
        self.csv_delimiter = ','
        self.set_start()

    def set_start(self):
        string_map = {v: int(ord(v) - 97) for v in list(string.ascii_lowercase)}
        fn_split = self.filename.strip().split('/')
        pref, suff = fn_split[-1].split('_')
        self.start = self.lines_to_be * string_map[suff]

    '''
    #Tried to use pandas  for faster file read:

    def read_csv(self):
        self.df = pandas.read_csv(self.filename, header=None, sep=self.csv_delimiter)
        self.df = self.df.fillna('NA')
        """
         The best case file is treated as data frame
        """

    def next(self):
        for row in self.df.iterrows():
            yield self.start, row[1]
            self.start += 1
    '''

    def read_csv(self):
        try:
            logging.info('reading the file {}'.format(self.filename))
            self.df = open(self.filename, 'r')
        except IOError, e:
            raise FileNotFound(e)

    def next(self):
        for row in self.df:
            yield self.start, row
            self.start += 1
