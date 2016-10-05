import getopt
import logging
import pprint
import sys
from multiprocessing import Manager, Process, cpu_count
from operator import itemgetter
from parser import ParseDoc

from filereader import DocProcess
from util import FileNotFound, NoArgumentException, Utility


class Worker(object):

    def __init__(self, fname, output_file):
        self.fname = fname
        self.split_files = None
        '''
        self.db_instance = Utility.tinydb_instance()
        '''
        self.undefined_list = Manager().list()
        self.defined_list = Manager().list()
        self.lines_to_be = 0
        self.output = {}
        self.opfile = output_file

    def data_process(self):
        """
        This method is to process the data. It will calculate the line count in file
        and split file based on line count. Now files are split to the number based on
        number of cores in machine.
        returns :Nothing
        """
        logging.info('Processing the data and split files')
        lines = Utility.file_len(self.fname)
        self.lines_to_be, self.split_files = Utility.split_files(self.fname, lines,
                                                                 cpu_count().real)

    def clean_json(self, line_no, row):
        """
        This method is for initial cleaning to reduce overhead from parser.
         Length of the Each line should be either 4 or 5 comma seperated
        :param line_no:  Line number from the file
        :param row: the document to process
        :return: Boolean
        """
        if len(row) not in [4, 5]:
            return False
        return True

    def parse_json(self, fname):
        """
        This is the core function. It will call ParseDoc object and parse each document
        The output is written to a shared memory list.
        :param fname:
        :return: Nothing
        """
        dp = DocProcess(fname, self.lines_to_be)
        dp.read_csv()
        parser_doc = ParseDoc()
        for line_no, row in dp.next():
            row_list = row.split(',')
            if self.clean_json(line_no, row_list):
                value = parser_doc.parse_machine(row_list)
                if value:
                    self.defined_list.append(value)
                else:
                    self.undefined_list.append(line_no)
            else:
                self.undefined_list.append(line_no)

    def mapper(self):
        workers = []
        for s_file in self.split_files:
            worker_process = Process(target=self.parse_json, args=(s_file, ))
            workers.append(worker_process)
            worker_process.start()

        [worker.join() for worker in workers]

    def reducer(self):
        self.output["entries"] = list(self.defined_list)
        self.output["errors"] = list(self.undefined_list)

        self.output["errors"].sort()
        new_list = sorted(self.output["entries"], key=itemgetter('lastname'))
        self.output["entries"] = new_list

        with open(self.opfile, 'w') as f:
            pprint.pprint(self.output, f, indent=2)

    def run(self):
        self.mapper()
        self.reducer()


def main(argv):
    try:
        if len(argv) == 0:
            logging.info('worker.py -i <inputfile> -o <outputfile>')
            raise NoArgumentException("No Argument is passed")

        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
        input_file = None
        output_file = None
        for opt, arg in opts:
            if opt == '-h':
                print 'worker.py -i <inputfile> -o <outputfile>'
                sys.exit()
            elif opt in ("-i", "--ifile"):
                input_file = arg
            elif opt in ("-o", "--ofile"):
                output_file = arg
    except getopt.GetoptError, e:
        logging.info('worker.py -i <inputfile> -o <outputfile>')
        raise e
    if not input_file or not output_file:
        logging.info('worker.py -i <inputfile> -o <outputfile>')
        raise NoArgumentException("One of  Argument is not passed")

    if Utility.is_file_exists(input_file):
        try:
            ws = Worker(input_file, output_file)
            ws.data_process()
            ws.run()
        except Exception, e:
            raise e
    else:
        raise FileNotFound(" The specified file does not present")

if __name__ == "__main__":
    main(sys.argv[1:])
