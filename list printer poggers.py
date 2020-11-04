fruit = ["banana","blueberry","lemon","melon","strawberry","apple"]
fruit.sort()
total = 0
for x in range(0, len(fruit)):
    print("[" + str(x+1) + "] " + fruit[x])
    total+= 1
print("    total: " + str(total))
