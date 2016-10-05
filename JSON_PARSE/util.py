import os
import subprocess
import logging


class FileNotFound(Exception):
    pass


class NoArgumentException(Exception):
    pass


class Utility(object):

    db_status = False

    @staticmethod
    def file_len(fname):
        p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        result, err = p.communicate()
        if p.returncode != 0:
            raise IOError(err)
        return int(result.strip().split()[0])

    @staticmethod
    def split_files(fname, linecount, divide):
        try:
            '''
             This part of code is to support for MAC. For linux
             there is already a option -d with split
             '''
            split_files_output = []
            savedPath = os.getcwd()
            os.system('mkdir -p /tmp/split_files')
            os.system('rm -rf /tmp/split_files/*')
            os.chdir('/tmp/split_files')
            lines_to_be = linecount / divide
            subprocess.call('split -a 1 -l {} {} F_'.format(lines_to_be, fname), shell=True)
            for (path, dirs, files) in os.walk('/tmp/split_files'):
                for file in files:
                    old_file = '/tmp/split_files/' + file
                    split_files_output.append(old_file)
            os.chdir(savedPath)
            return lines_to_be, split_files_output
        except IOError, e:
            raise e

    @staticmethod
    def tinydb_instance():
        """
        Initially idea was  to use TinyDB as internal shared memory. TinyDB is lighweight.
        But it errors while running in parallel environment.
        Code is present but unused.
        """
        from tinydb import Query, TinyDB
        if not Utility.db_status:
            os.system('rm -rf /tmp/db.json')
            Utility.db_status = True
        try:
            return TinyDB('/tmp/db.json')
        except Exception as e:
            raise e

    @staticmethod
    def tinydb_write(db_instance, value):
        try:
            from tinydb import Query, TinyDB
            db_instance.insert(value)
        except Exception, e:
            logging.debug('the value to be inserted is {}'.format(value))
            raise e

    @staticmethod
    def tinydb_query(db_instance):
        user = Query()
        return db_instance.search(user.lineno >= 1)

    @staticmethod
    def is_file_exists(fname):
        import os.path
        return os.path.isfile(fname)
