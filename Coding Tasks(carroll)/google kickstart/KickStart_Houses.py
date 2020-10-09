def getinputs():    
    tmpN,tmpB = input("please enter N and B, in format 'N B'").split( )
    N = int(tmpN)
    B = int(tmpB)
    Alist = input("please enter " + str(N) + " values for A, in format 'A A'").split(" ",N-1)
    return N,B,Alist

def getnumber(A, B):
    counter = 0
    validhouses = 0
    while counter < int(len(A)):
        if B >= int(A[counter]):
            validhouses += 1
            B -= int(A[counter])
            counter += 1
        else:
            counter = 10000
    return validhouses

T = int(input("please enter the test cases (T)"))
Case = 1

while Case <= T:
    N,B,Alist = getinputs()
    Alist.sort(reverse=False)
    print("Case #" + str(Case) + ": " + str(getnumber(Alist,B)))
    Case += 1        
