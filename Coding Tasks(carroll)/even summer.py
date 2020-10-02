def sumEven(tempN,n,sumN):
    if (tempN <= n) and (n % 2 == 0):
        sumN += tempN
        tempN += 2
        return sumEven(tempN,n,sumN)
    else:
        return sumN
    #end if
#end sub

print("sum of 10: " + str(sumEven(0,10,0)))
