from lx16a import *
import time
import numpy as np

LX16A.initialize("/dev/ttyUSB0", 0.1)

minN = 1
maxN = 9

servos = [0]

try:
    for i in range(minN, maxN):
        servos.append(LX16A(i))
        servos[i].enable_torque()
        # print(servos[i].is_torque_enabled())

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

# Amplitudes of trig functions
# a = 10
# b = 10

# a=10, b=15 kind of works... kind of
a = 10
b = 15

# Exageratting the push-up
# a = 20
# b = 30

# Sets t parameteric variable for more manual sin movement
t=0

# Works with for loop below
tsin = 0.25
tcos = 0

time_step = 0.5

startingAngles = np.array([0., 120., 74.88, 177.6, 73.44, 119.76, 126.48, 171.36, 90.72])

goalAngles = np.zeros((int(1/time_step),9))

# This just generates a pushup movement for some reason
for j in range(int(1/time_step)):
    for i in range(minN, maxN):
        if i == 1 or i == 7:
            goalAngles[j][i] = np.sin(2*np.pi*tsin)*a + startingAngles[i]
        elif i == 2 or 8:
            goalAngles[j][i] = np.cos(2*np.pi*tcos)*b + startingAngles[i]
        elif i == 3 or i == 5:
            goalAngles[j][i] = np.cos(2*np.pi*tsin)*a + startingAngles[i]
        elif i == 4 or i == 6:
            goalAngles[j][i] = np.sin(2*np.pi*tcos)*b + startingAngles[i]
    tsin += time_step
    tcos += time_step
        
# move_time = 100

while True:
    try:
        # # Listing out explicitly while I figure it out
        # # This one it slips and doesn't really push forward at all
        servos[1].move(np.sin(2*np.pi*t)*a + 120)#, time=move_time)
        servos[2].move(np.cos(2*np.pi*t)*b + 75)#, time=move_time)

        servos[3].move(np.cos(2*np.pi*t)*a + 177)#, time=move_time)
        servos[4].move(np.sin(2*np.pi*t)*b + 73)#, time=move_time)

        servos[5].move(np.cos(2*np.pi*t)*a + 120)#, time=move_time)
        servos[6].move(np.sin(2*np.pi*t)*b + 126)#, time=move_time)

        servos[7].move(np.sin(2*np.pi*t)*a + 170)#, time=move_time)
        servos[8].move(np.cos(2*np.pi*t)*b + 90)#, time=move_time)

        # This just does pushups for some reason
        # for j in range(int(1/time_step)):
        #     for i in range(minN, maxN):
        #         servos[i].move(goalAngles[j][i], time = 1000)
        #     time.sleep(1)

    # Handle servos timing out
    except ServoTimeoutError as e:
        print(f"While loop: Servo {e.id_} is not responding. Exiting...")
        quit()
    
    t+=0.1
    time.sleep(0.05)
    