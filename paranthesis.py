'''
Print all combinations of balanced parentheses
Write a function to generate all possible n pairs of balanced parentheses.

For example, if n=1
{}
for n=2
{}{}
{{}}
'''

def paranthesis(sizes, lcount, rcount, output):
     if lcount == sizes and rcount == sizes:
         print ''.join(output)
         return

     if lcount < sizes:
         output.append('{')
         paranthesis(sizes, lcount + 1, rcount, output)
         output.pop()

     if rcount < lcount:
         output.append('}')
         paranthesis(sizes, lcount, rcount + 1, output)
         output.pop()


paranthesis(3, 0, 0, [])
