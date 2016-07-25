import hashlib

def read_file(filename,hashmap,hashdata):

      for flines in open(filename):
            #flines = f.readlines()    #reading file
            flines=flines.strip() #strip remove extra space or \n at end
            lines = flines.split() #split by space
            tobehashed = flines[len(lines[0]):]
            #print 'tobehashed',tobehashed
            data  = hashlib.md5(tobehashed).hexdigest()
            hashmap[lines[0].lower()] = data
            if data in hashdata:
                hashdata[data] +=1
                hashdata_set[data].append(lines[0].lower())
            else:
                hashdata[data] = 0 #this one contains another dictionary
                hashdata_set[data]=[]



hashmap={}
hashdata={}
hashdata_set = {}

read_file('cmudict.txt',hashmap,hashdata)
#print hashdata

print hashdata[hashmap['too']]
print hashdata_set[hashmap['too']]

for k,v in sorted(hashdata.items(), key=lambda i: i[1]):
    print hashdata_set[k],' : ', v
