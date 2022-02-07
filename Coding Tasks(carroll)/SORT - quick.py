import math
import random

numpog = []
cap = 1000

i = 0
while i <= cap:
    numpog.append(random.randint(1,cap))
    i+=1

def sort(numbers):
    sorted = []

    while len(sorted) < len(numbers):
        if len(sorted) == 0:
            key = len(numbers)//2
        elif len(sorted) <= len(numbers)//2:
            key = sorted[len(sorted)-1] - 1 // 2
        else:
            key = (len(numbers) - sorted[:1]) // 2
        left = 0
        right = len(numbers) - 1
        sorted.append(key)
        while left < right:
            while numbers[left] < numbers[key]:
                left += 1
            while numbers[right] > numbers[key]:
                right -= 1
            temp = numbers[left]
            numbers[left] = numbers[right]
            numbers[right] = temp
    
    return(numbers)

print("1")
print(sort(numpog))
print("2")                
        
