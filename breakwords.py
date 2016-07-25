'''
Given a string s and a dictionary of words dict, add spaces in s to construct a sentence where each word is a valid dictionary word.

Return all such possible sentences.

For example, given
s = "catsanddog",
dict = ["cat", "cats", "and", "sand", "dog"].

A solution is ["cats and dog", "cat sand dog"]
'''


def findword(tdict, input, ln, words, position):
       if len(input) == 0:
           print ' '.join(words)
           return
       for i in range(len(input)+1):
           tstr = input[0:i]
           if tstr in tdict:
               words.append(tstr)
               findword(tdict, input[i:], ln, words, position)
               words.pop()

def findwords(tdict, input, ln, words, start, position):
    if input:
       if ln == len(input)+1:
           print words
           return
       tstr = input[start:ln]
       if tstr in tdict:
           if tstr not in position:
               words.append(tstr)
               position.add(tstr)
               start = ln
           else:
               start = ln + 1
       findwords( tdict, input, ln+1, words, start, position)


tdict = ["cat", "cats", "and", "sand", "dog"]
#findwords(tdict, "catsanddog", 0, [], 0, set())
findword(tdict, "catsanddog", 0, [], set())