array = [11,32,42,54,31,22,3,4,521,233,242,12]

def Lsearch(newarray,tofind):
    if newarray[0] == tofind:
        return 0
    else:
        return Lsearch(newarray[1:],tofind) + 1


print(Lsearch(array,11))
    
