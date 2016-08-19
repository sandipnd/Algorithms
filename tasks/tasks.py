'''

Using python task framework to schedule job
'''

import time
import Queue

from threading import Thread
from tasks.task import Task

PENDING = 'PENDING'
EXECUTING = 'EXECUTING'
CHECKING = 'CHECKING'
FINISHED = 'FINISHED'

class Task(Future):
    def __init__(self, name):
        Future.__init__(self)
        self.log = logger.Logger.get_logger()
        self.state = PENDING
        self.name = name
        self.cancelled = False
        self.retries = 0
        self.res = None

    def step(self, task_manager):
        if not self.done():
            if self.state == PENDING:
                self.state = EXECUTING
                task_manager.schedule(self)
            elif self.state == EXECUTING:
                self.execute(task_manager)
            elif self.state == CHECKING:
                self.check(task_manager)
            elif self.state != FINISHED:
                raise Exception("Bad State in {0}: {1}".format(self.name, self.state))

    def execute(self, task_manager):
        raise NotImplementedError

    def check(self, task_manager):
        raise NotImplementedError


class TaskManager(Thread):
    def __init__(self, thread_name=None):
        Thread.__init__(self)
        self.readyq = Queue.Queue()
        self.sleepq = Queue.Queue()
        self.running = True
        if thread_name is not None:
            self.name = thread_name

    def schedule(self, task, sleep_time=0):
        if not isinstance(task, Task):
            raise TypeError("Tried to schedule somthing that's not a task")
        if sleep_time <= 0:
            self.readyq.put(task)
        else:
            wakeup_time = time.time() + sleep_time
            self.sleepq.put({'task': task, 'time': wakeup_time})

    def run(self):
        while (self.running == True or self.readyq.empty() != True or self.sleepq.empty() != True):
            if self.readyq.empty():
                time.sleep(1)
            else:
                task = self.readyq.get()
                task.step(self)
            for i in range(self.sleepq.qsize()):
                s_task = self.sleepq.get()
                if time.time() >= s_task['time']:
                    self.readyq.put(s_task['task'])
                else:
                    self.sleepq.put(s_task)

    def shutdown(self, force=False):
        self.running = False
        if force:
            while not self.sleepq.empty():
                task = self.sleepq.get()['task']
                task.cancel()
                self.readyq.put(task)
            while not self.readyq.empty():
                try:
                    task = self.readyq.get()
                    task.cancel()
                except Exception, ex:
                    raise ex