import math
import random

numbers = []
cap = 1000

i = 0
while i <= cap:
    numbers.append(random.randint(1,cap))
    i += 1

i -= 1

storednum = 0

while i > 0:
    j = 0
    while j < i:
        if numbers[j] >  numbers[j+1]:
            storednum = numbers[j+1]
            numbers[j+1] = numbers[j]
            numbers[j] = storednum
        j += 1
    i -= 1

print(numbers)
