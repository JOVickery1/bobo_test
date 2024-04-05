from lx16a import *
import time
import numpy as np

LX16A.initialize("/dev/ttyUSB0", 0.1)

minN = 1
maxN = 9

servos = [0]
# Testing if I need to enter this damn passphrase

try:
    for i in range(minN, maxN):
        servos.append(LX16A(i))
        servos[i].enable_torque()
        # print(servos[i].is_torque_enabled())

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

# a=10, b=15 kind of works... kind of
a = 10
b = 15

# Sets t parameteric variable for more manual sin movement
# Not using anymore
t=0

# Works with for loop below
# Sets different starting times for the trig functions
# Could also be accomplished with offsets
tsin = 0.25
tcos = 0

time_step = 0.5

startingAngles = np.array([0., 120., 74.88, 177.6, 73.44, 119.76, 126.48, 171.36, 90.72])

goalAngles = np.zeros((int(1/time_step),9))

# this just generates angles for pushups for some reason
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
        

homeAngle = np.array([0., 120., 74.88, 177.6, 73.44, 119.76, 126.48, 171.36, 90.72])

try:
    # Iterate through motors 1 to 8
    for i in range(minN, maxN):
        '''# Get current physical angle
        # currentAngle.append(servos[i].get_physical_angle())'''

        # Move motor to its goal angle
        servos[i].move(homeAngle[i], wait=True, time = 1500)

        '''# Print the currentAngle array once it is fully populated
        # if i == maxN:
        #     print(currentAngle)'''

    # Set motors to move "simultaneously"
    # not technically simultaneous, but marginally closer to it than doing so without wait=True
    for i in range(minN,maxN):
        servos[i].move_start()

    '''# # Set motors moving to true
    # motorsMoving = True'''
    # Sleep for enough time for motors to finish homing
    time.sleep(1.5)

# Handle servos timing out
except ServoTimeoutError as e:
    print(f"MOVE ERROR: Servo {e.id_} is not responding. Exiting...")
    quit()

freq=2*np.pi
# freq = 1

'''move_time = #Something'''

while True:
    try:
        # # Listing out explicitly while I figure it out
        # # This one it slips and doesn't really push forward at all
        servos[1].move(np.sin(freq*t)*a + 120)#, time=move_time)
        servos[2].move(np.cos(freq*t)*b + 75)#, time=move_time)

        servos[3].move(np.cos(freq*t)*a + 177)#, time=move_time)
        servos[4].move(np.sin(freq*t)*b + 73)#, time=move_time)

        servos[5].move(np.cos(freq*t)*a + 120)#, time=move_time)
        servos[6].move(np.sin(freq*t)*b + 126)#, time=move_time)

        servos[7].move(np.sin(freq*t)*a + 170)#, time=move_time)
        servos[8].move(np.cos(freq*t)*b + 90)#, time=move_time)

        '''# This just does pushups for some reason
        # for j in range(int(1/time_step)):
        #     for i in range(minN, maxN):
        #         servos[i].move(goalAngles[j][i], time = 1000)
        #     time.sleep(1)'''

    # Handle servos timing out
    except ServoTimeoutError as e:
        print(f"While loop: Servo {e.id_} is not responding. Exiting...")
        quit()
    
    # works well for freq = 2pi
    t+=0.1
    time.sleep(0.05)
        
    # t+=0.01
    # time.sleep(0.001) 