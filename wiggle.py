'''
A sequence of numbers is called a wiggle sequence if the differences between successive numbers strictly alternate between positive and negative. The first difference (if one exists) may be either positive or negative. A sequence with fewer than two elements is trivially a wiggle sequence.

For example, [1,7,4,9,2,5] is a wiggle sequence because the differences (6,-3,5,-7,3) are alternately positive and negative. In contrast, [1,4,7,2,5] and [1,7,4,5,5] are not wiggle sequences, the first because its first two differences are positive and the second because its last difference is zero.

Given a sequence of integers, return the length of the longest subsequence that is a wiggle sequence. A subsequence is obtained by deleting some number of elements (eventually, also zero) from the original sequence, leaving the remaining elements in their original order.
'''

class Solution(object):
    def trackstate(self, v1, v2):
        op = v1 - v2
        if op > 0:
            state = '+ve'
        else:
            state = '-ve'
        return state

    def wiggleMaxLength(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        count = 0
        if len(nums) >= 2:
            mystate = {}
            mystate['+ve'] = '-ve'
            mystate['-ve'] = '+ve'

            state=self.trackstate(nums[0], nums[1])
            nextstate = mystate[state]
            count += 1
            j = 1
            while j+1 < len(nums):
                state = self.trackstate(nums[j], nums[j+1])
                if state == nextstate:
                    #print state, nextstate, nums[j], nums[j+1]
                    count += 1
                nextstate = mystate[state]
                j += 1
        return count

a = Solution()
print a.wiggleMaxLength([1,7,4,9,2,5])
print a.wiggleMaxLength([1,17,5,10,13,15,10,5,16,8])
print a.wiggleMaxLength([1,2,3,4,5,6,7,8,9])