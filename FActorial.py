def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
    #end if
#end function

number=input("please enter what you want to factorialise \n")
print(factorial(int(number)))

print("0: " + str(factorial(0)))
    
