import math
import random

numpog = []
cap = 1000

i = 0
while i <= cap:
    numpog.append(random.randint(1,cap))
    i+=1

def split(numbers):
    if len(numbers) == 1:
        return numbers
    else:
        merged = []
        middle = len(numbers) // 2
        list1 = split(numbers[:middle])
        loc1 = 0
        list2 = split(numbers[middle:])
        loc2 = 0
        while loc1 < len(list1) or loc2 < len(list2):
            if loc2 >= len(list2):
                merged.append(list1[loc1])
                loc1 += 1
            elif loc1 >= len(list1):
                merged.append(list2[loc2])
                loc2 += 1
            else:
                if list1[loc1] <= list2[loc2]:
                    merged.append(list1[loc1])
                    loc1 += 1
                else:
                    merged.append(list2[loc2])
                    loc2 += 1
        return merged

print(split(numpog))
                
        
