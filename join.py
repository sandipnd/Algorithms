'''
 Trying map reduce 
Sample Input

Department,1234,Sales
Employee,Susan,1234
Department,1233,Marketing
Employee,Joe,1233
Department,1233,Accounts
Sample Output

('1233', 'Joe', 'Accounts')
('1233', 'Joe', 'Marketing')
('1234', 'Susan', 'Sales')

'''
import sys
from collections import OrderedDict
from itertools import groupby
from itertools import cycle

class MapReduce:
    def __init__(self):
        self.intermediate = OrderedDict()
        self.result = []
   

    def emitIntermediate(self, key, value):
      self.intermediate.setdefault(key, [])       
      self.intermediate[key].append(value)

    def emit(self, value):
        self.result.append(value) 

    def execute(self, data, mapper, reducer):
        for record in data:
            mapper(record)

        for key in self.intermediate:
            reducer(key, self.intermediate[key])

        self.result.sort()
        for item in self.result:
            print item

mapReducer = MapReduce()

def mapper(record):
    #Start writing the Map code here
    s=record.split(',')
    if s[0] == 'Department':
       ssn = s[1]    
       mapReducer.emitIntermediate(ssn, ('dept', s[2]))
    else:
       ssn = s[2]    
       mapReducer.emitIntermediate(ssn, ('name', s[1]))                            
    

def reducer(key, list_of_values):
    #Start writing the Reduce code here
    
    dept=[]
    name=[]
    for key1, group in groupby(list_of_values, lambda x: x[0]):
        for thing in group:
            if key1 == 'dept':
                dept.append(thing[1])
            else:
                name.append(thing[1])
    dept.sort()
    for v in zip(cycle(name), dept):
        result=(key, ) + v
        mapReducer.emit(result)
    
            
if __name__ == '__main__':
  inputData = ['Department,1233,Aarketing','Employee,Joe,1233','Department,1233,Accounts','Department,1234,Sales', 'Employee,Susan,1234' ]
  #for line in sys.stdin:
   #inputData.append(line)
  mapReducer.execute(inputData, mapper, reducer)

