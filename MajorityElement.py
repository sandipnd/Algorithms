var = [5,2,4,1,6,2,2,2,2,1,5]

'''
https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_majority_vote_algorithm
Given an array of size n, find the majority element. The majority element is the element that appears more than n/2  times
You may assume that the array is non-empty and the majority element always exist in the array.
'''

def findmajority(var):

    count = 0
    major = None

    for v in var:
        if count == 0 :
            major = v
            count = 1

        elif major == v:
            count += 1

        elif major != v:
            count -= 1

    print major

findmajority(var)
