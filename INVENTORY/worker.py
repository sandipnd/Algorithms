from multiprocessing import Process, Queue, Lock
from inventorygen import datastore, myIterator


class reader:

    def __init__(self,db):
        self.dbobject = db

    def run(self,queue, lock):
        self.val = queue.get()


    def processdata(self):



class worker(object):
      def __init__(self, invenworker, data, reader):
          self.invenallocnum = invenworker
          self.data =  data
          self.readernum = reader
          self.q = Queue()
          self.db = datastore(data)
          self.lock = Lock()
          self.workers = []
          self.allocator=myIterator(self.d)
          self.reader = reader(self.db)

      def start_workers(self):
          for i in range( self.invenallocnum):
              p=Process(target=self.allocator.run,args=(self.q))
              p.start()
              self.workers.append(p)

          for i in range(self.readernum):
              p=Process(target=self.allocator.run,args=(self.q, self.lock))
              p.start()
              self.workers.append(p)

      def wait_for_workers(self):
          for w in self.workers:
              w.join()
              if w.exitcode:
                  pass


