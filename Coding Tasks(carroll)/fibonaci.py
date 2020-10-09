def fibonacci(n):
    fibNumbers = [1,1]
    for i in range(2 , n):
        fibNumbers.append(fibNumbers[i-1] + fibNumbers[i-2])
    print(fibNumbers)
    return fibNumbers[n-1]

print(fibonacci(2102020))
