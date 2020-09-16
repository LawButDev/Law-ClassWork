inputno = 0;
name = "youdonemessedupyourcodesomewhere"
num1 = 0;
start_num = 0;
end_num = 0;
mini_loop = True;
row = 0
invalid_number = False


def multiples(name,num1,num2,num3):
    row = num2;
    print(name + " here is your times table")
    while row <= num3:
        print("(" + str(num1) + "*" + str(row) + ") = " + str(num1 * row))
        row += 1
    #end while

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
           inputno = int(input("please enter the start number you want (1 or more) "))
           invalid_number = False
        except ValueError:
            print("invalid number, try again")
    #end while
    if (inputno >= 1):
        choicetext = input("you have chosen " + str(inputno) + " as your start number if you want to keep this number please enter y ")
        if choicetext == "y":
            start_num = inputno
            mini_loop = False
        #endif
    else:
        print("please enter a number bigger than 1")
    #end if
 #endwhile
        
mini_loop = True
while mini_loop == True:
    invalid_number = True
    while invalid_number:
        try:
           inputno = int(input("please enter the end number you want (bigger than your start number) "))
           invalid_number = False
        except ValueError:
            print("invalid number, try again")
    #end while
    if (inputno > start_num):
        choicetext = input("you have chosen " + str(inputno) + " as your start number if you want to keep this number please enter y ")
        if choicetext == "y":
            end_num = inputno
            mini_loop = False
        #endif
    else:
        print("please enter a number bigger than your start number")
    #end if
 #endwhile

multiples(name,num1,start_num,end_num)


