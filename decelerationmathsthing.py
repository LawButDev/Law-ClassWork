deceleration = 2.25
stoppingdistance = 0
speed = 25
time = 0

while speed > 0:
    stoppingdistance += ((speed + (speed - deceleration))/2)
    speed -= deceleration
    time += 1

print(time)
print("stop" + str(stoppingdistance))

speed = 20
stoppingdistance = 0

while time > 0:
    stoppingdistance += (speed * 2 - deceleration) / 2
    speed += deceleration 
    time -= 1

print("dist" + str(stoppingdistance))
print("spd" + str(speed))
    
