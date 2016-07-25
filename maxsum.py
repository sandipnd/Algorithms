'''
Given a list of non negative integers, arrange them such that they form the largest number.

For example, given [3, 30, 34, 5, 9], the largest formed number is 9534330
'''
def comparator(a, b):
    x = str(a) + str(b)
    y = str(b) + str(a)
    if x > y:
        return 1
    return -1

def maxsum():
    mylist = [3, 30, 34, 5, 9]
    mylist=sorted(mylist, cmp = comparator, reverse=True)
    print ''.join(str(x) for x in mylist)