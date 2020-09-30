def inputname():
    global Names
    subbool = True
    while subbool:
        name = input("please enter the name to enter it into the list \n")
        position = int(input("please enter a position in the list to insert the name (1-10): \n"))
        if position >= 1 and position <= 10:
            Names[position-1] = name
            subbool = False
        else:
            print("input is invalid, please try again")
        #end if
    #end while
#end sub

def displayname():
    global Names
    counter = 1
    print("")
    while counter <= 10:
        print("(" + str(counter) + ") - " + str(Names[counter-1]))
        counter = counter + 1
    #end while
    print("")
#end sub
    

def display_menu():
    global Names
    Names = ['','','','','','','','','','']
    mainbool = True
    while mainbool:
        choice = int(input("please enter one of the following three choices \n" \
                       "(1) - Add Name \n" \
                       "(2) - Display List \n" \
                       "(3) - Quit \n" ))
        if choice < 1 or choice > 3:
            print("number is invalid, please try again \n")
        elif choice == 1:
            inputname()
        elif choice == 2:
            displayname()
        elif choice == 3:
            print("k bye")
            mainbool = False
        #end if
    #end while
#end sub              
            

global Names
display_menu()
