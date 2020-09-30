inputno = 0;
num1 = 0;
num2 = 0;
mini_loop = True;
row = 0
invalid_number = False

mini_loop = True
while mini_loop == True:
    invalid_number = True
    while invalid_number:
        try:
           inputno = int(input("please enter the times table you want (1-20) "))
           invalid_number = False
        except ValueError:
            print("invalid number, try again")
    #end while
    if (inputno >= 1 and inputno <= 20):
        choicetext = input("you have chosen the " + str(inputno) + " times table if you want to keep this number please enter y ")
        if choicetext == "y":
            num1 = inputno
            mini_loop = False
        #end if
    else:
        print("please enter a valid times table between 1 and 20")
    #end if
    
#endwhile
mini_loop = True
while mini_loop == True:
    invalid_number = True
    while invalid_number:
        try:
           inputno = int(input("please enter the ammount of rows you want (1 or more) "))
           invalid_number = False
        except ValueError:
            print("invalid number, try again")
    #end while
    if (inputno >= 1):
        choicetext = input("you have chosen " + str(inputno) + " row(s) if you want to keep this number please enter y ")
        if choicetext == "y":
            num2 = inputno
            mini_loop = False
        #endif
    else:
        print("please enter a number bigger than 1")
    #end if
 #endwhile
row = 1;
while row <= num2:
    print ("(" + str(num1) + "*" + str(row) + ") = " + str(num1 * row))
    row += 1
#end while

