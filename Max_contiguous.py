'''
Given a binary array, find the maximum length of a contiguous subarray with equal number of 0 and 1.

Example 1:
Input: [0,1]
Output: 2
Explanation: [0, 1] is the longest contiguous subarray with equal number of 0 and 1.
Example 2:
Input: [0,1,0]
Output: 2
Explanation: [0, 1] (or [1, 0]) is a longest contiguous subarray with equal number of 0 and 1.

'''

def findMaxLength(nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        v= [-1 if x==0 else x for x in nums]
        print v
        cur_len = 0
        max_len = 0
        sum = 0
        index = 0
        sum_present = {}
        while index < len(v):
            sum += v[index]
            cur_len += 1
            if sum == 0:
                if max_len < cur_len:
                    max_len = cur_len

            if sum in sum_present:
                max_len = max(max_len, index - sum_present[sum])
            else:
                sum_present[sum] = index
            index += 1
        return max_len
