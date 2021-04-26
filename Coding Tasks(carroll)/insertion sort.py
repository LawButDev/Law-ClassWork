import math
import random

numbers = []
cap = 1000

sorted = []

i = 0
while i <= cap:
    numbers.append(random.randint(1,cap))
    i+=1


j = 1
sorted.append(numbers[0])

while j <= cap:
    stored = numbers[j]
    inserted = False
    k = len(sorted) - 1
    sorted.append(9999)
    while not inserted:
        if k >= 0:
            if stored < sorted[k]:
                sorted[k+1] = sorted[k]
                sorted[k] = 0
                k -= 1
            else:
                sorted[k+1] = stored
                inserted = True
        else: inserted = True
            
    j += 1


print(sorted)
