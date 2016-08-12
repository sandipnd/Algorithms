'''
Given an array with n objects colored red, white or blue, sort them so that objects of the same color are adjacent, with the colors in the order red, white and blue.
Here, we will use the integers 0, 1, and 2 to represent the color red, white, and blue respectively.
Note: You are not suppose to use the library's sort function for this problem.
'''

def sortcolor(colorlist):

    if colorlist:
        start = 0
        end = len(colorlist) - 1
        mid = 0

        while mid < end:
            #print mid
            if colorlist[mid] == 0:
                colorlist[mid], colorlist[start] = colorlist[start], colorlist[mid]
                #print colorlist
                mid += 1
                start += 1
            elif colorlist[mid] == 1:
                mid += 1
            elif colorlist[mid] == 2:
                colorlist[mid], colorlist[end] = colorlist[end], colorlist[mid]
                end -= 1


        print colorlist

colorlist = [0,1,2,2,0,0,0,2,1,1,2,0,1]
sortcolor(colorlist)