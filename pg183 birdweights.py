def weightcalc(average,routecontrol):
    weight = [1500,3000,4500,2000,1579,2003,4500,4500,4500,4500]
    total = 0
    totalunder = 0
    countunder = 0
    for i in range(0,9):
        total+= weight[i]
        if weight[i] + 500 < average:
            totalunder += weight[i]
            countunder += 1
        #end if
    #next
    if routecontrol > 0:
        print("overall average: " + str(total/9))
        return(total/9)
    elif routecontrol < 0:
        print("underweight average: " + str(totalunder/countunder))
        print("underweight count: " + str(countunder))
    #end if
#end sub

weightcalc(weightcalc(0,1),-1)
