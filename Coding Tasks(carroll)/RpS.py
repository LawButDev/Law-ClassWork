### SRC - A good idea, but please update on the basis of what you saw in class
from random import *

def checker(pchoice,cchoice):
    if int(pchoice) == int(cchoice):
        print("its a draw")
    elif (int(pchoice) > int(cchoice)) and (not((pchoice == 3) and (cchoice == 1))):
        #if pchoice == 3 and cchoice == 1:
        #    print("P2 Wins")
        #else:
            print("P1 Wins")
    else:
        print("P2 Wins")

mainbool = True
while mainbool:
    print("\n rock = 1 \n paper = 2 \n scissors = 3 \n")
    choice = input("please enter p1's choice:  ")
    choice2 = input("please enter p2's choice:  ")
    #choice2 = randint(1,3)
    print(choice2)
    print("")
    checker(choice,choice2)

    
