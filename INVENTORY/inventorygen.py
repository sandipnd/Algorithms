import json
import itertools
from myexception import invalidDataException
from random import randint, random

class datastore(object):
    '''
     Creating the datastore for the inventory
    '''
    def __init__(self, data):
        self.store = data
        self.count = 0
        self.maxvalue = 0
        self.storedata()

    def storedata(self):
        flag = False
        for k,v in self.store.iteritems():
            if v > self.maxvalue:
                self.maxvalue  = v
            if v < 0:
                raise invalidDataException("Inventory count "
                                        "is -ve ")
            if v:
                flag = True
        if not flag:
            raise invalidDataException(" All Inventory count "
                                           "is 0 ")

    def getdata(self):
        return self.store

    def getcount(self):
        return self.count

    def getmax(self):
        return self.getmax


class randomgen:

    def randomheader(self):
        return int(100 * random())

    def randomquant(self, maxsize):
        return randint(0,maxsize)

    def randomproduct(self, size):
        return randint(0,size)

    def randomProductNum(self):
        return randint(1,2)


class myIterator(object):
    def __init__(self, dataobj):
        self.db = dataobj
        self.inventory = dataobj.getdata().keys()
        self.inventorycount = 0
        self.invintorysize =  len(self.inventory)
        self.quantmax = dataobj.getmax()
        #{"Header": 1, "Lines":
        # {"Product": "A", "Quantity": "1"}{"Product": "C", "Quantity": "1"}}

    def inventorygen(self):
        inventorylist = {}
        templist = []
        inventorylist['header'] = randomgen.randomheader()
        myrange = randomgen.randomProductNum()
        for i in range(myrange):
            tmp = {}
            tmp['Product'] = self.inventory[randomgen.randomproduct()]
            tmp['quantity'] = randomgen.randomquant(self.quantmax)
            templist.append(tmp)

        inventorylist['List'] = templist
        return inventorylist

    def run(self, queue):
        while True and self.db.getcount():
            queue.add(self.inventorygen())

