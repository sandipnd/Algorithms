'''
Given a digit string, return all possible letter combinations that the number could represent.
A mapping of digit to letters (just like on the telephone buttons) is given below.

Input:Digit string "23"
Output: ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].
'''

def phonenumber(pmap, input, index, output):
     if index == len(input):
         print ''.join(output)
         return

     for v in pmap[input[index]]:
         output.append(v)
         #print output
         phonenumber(pmap, input, index + 1, output)
         output.pop()

alphs = ["","", "abc", "def", "ghi", "jkl", "mno","pqrs","tuv", "wxyz"]
pmap = {str(k): v for k,v in enumerate(alphs)}
phonenumber(pmap, '23', 0, [])
