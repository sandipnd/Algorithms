'''
Given a string S, find the all palindromic substring in S
'''
def countpalindrome(pstr, start, end):
    count  = 0
    while start >= 0 and end < len(pstr):
        #print start, end
        if pstr[start] != pstr[end]:
            break
        print pstr[start:end+1]
        start -= 1
        end += 1
        count += 1

    return count

def palindrome(pstr):
   plen = len(pstr)
   i = 0
   for i in range(plen/2):
       countpalindrome(pstr, i-1, i+1)
       countpalindrome(pstr, i, i+1)
       i += 1

palindrome('aabbaa')