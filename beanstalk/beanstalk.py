import beanstalkc
import pickle
import os
from decorator import decorator
import time
import logger
import threading

@decorator
def retry(method, *args, **kwargs):
    for i in range(5):
        try:
            method(*args, **kwargs)
            return
        except Exception:
            queueManager().teardown()
            time.sleep(10)
            pass

class queueManager(object):

    '''
     Objective is to craete a Singleton class
     http://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons-in-python
    '''
    _instance = None
    log = logger.Logger.get_logger()
    '''
    keep lock as like this. Writing like this will enforce
    as static variable which will be shared across class
    '''
    lock = threading.Lock()
    def  __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(queueManager, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    @retry
    def startService(port):
        queueManager.log.info(" starting beanstalkc service on port {}".format(port))
        os.system('nohup beanstalkd -l 127.0.0.1 -p {} &'.format(port))

    @staticmethod
    def get_client(bucketname, newport):
        beanstalk = beanstalkc.Connection(host='localhost', port=newport)
        #beanstalk.use(bucketname)
        #beanstalk.watch(bucketname)
        return beanstalk

    @staticmethod
    def producer(client, key, value, priority):
        '''
         the input of producer is string,
         https://github.com/earl/beanstalkc/blob/master/TUTORIAL.mkd
         So pickle with convert json to string
        '''
        picklestring = pickle.dumps((key, value))
        client.put(picklestring)

    @staticmethod
    def consumer(client, queuename, debug=False):
        with queueManager.lock:
            if queueManager().isQEmpty(client, queuename):
                client.ignore(queuename)
                return "End", "End"
        job = client.reserve()
        value = job.body
        job.delete()
        key, value = pickle.loads(value)
        if debug:
          queueManager().check_status(job)
        return key, value

    @staticmethod
    def close(client):
        client.close()

    @staticmethod
    def teardown():
        queueManager.log.info(" Killing beanstalkd service")
        os.system("killall -9 beanstalkd")

    @staticmethod
    def check_status(job):
        queueManager.log(job.status())

    @staticmethod
    def isQEmpty(client, queuename):
        stats = client.stats_tube('default')
        #print stats
        return stats['current-jobs-ready'] == 0

    def __enter__(self):
        self.client = beanstalkc.Connection(host='localhost', port=14711)
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

