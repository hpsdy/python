#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
二分查找
'''
def q(arr,key):
    arr = sorted(arr)
    print(arr)
    start = 0
    end = len(arr)-1
    while(start<=end):
        mid = (start+end)//2
        midVal = arr[mid]
        if midVal==key:
            return mid
        elif midVal>key:
            end = mid-1
        else:
            start=mid+1
    return -1

arr = [1,33,55,11,2,3,5,2,8,10]
print(q(arr,2))

def BinarySearch(haystack, needle):
  low = 0
  high = len(haystack) - 1
  while(low <= high):
    mid = (low + high)//2
    midval = haystack[mid]
    if midval < needle:
      low = mid + 1
    elif midval > needle:
      high = mid - 1
    else:
      print(mid)
      return mid
  print(-1)
  return -1
if __name__ == "__main__":
  haystack = [int(i) for i in list("123456789")]
  needle = 8
  BinarySearch(haystack ,needle)