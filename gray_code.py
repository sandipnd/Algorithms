def gengraycode(n, mylist, bits):
   newlist = []
   if bits == n+1:
       return mylist
   i = 0

   while i < len(mylist):
     newlist.append('0'+ mylist[i])
     i += 1
   mylist = mylist[::-1]

   i = 0
   while i < len(mylist):
       newlist.append('1'+ mylist[i])
       i += 1
   #print newlist
   return gengraycode(n, newlist, bits + 1)


def porcess(values):
    result = []
    for v in values.split('|'):
        val = v.strip()
        mylist = ['0', '1']
        finals = gengraycode(len(val), mylist, 2)
        maps = {}
        for k,v1 in enumerate(finals):
           maps[v1] = k
        result.append(str(maps[val]))

    print ' | '.join(result)


porcess('1111 | 1110')
porcess('10 | 1100001 | 101')

