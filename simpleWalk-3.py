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

homeAngle = np.array([0., 120., 74.88, 177.6, 73.44, 119.76, 126.48, 171.36, 90.72])

try:
    # Iterate through motors 1 to 8
    for i in range(minN, maxN):
        # Move motor to its goal angle
        servos[i].move(homeAngle[i], wait=True, time = 1500)

    # Set motors to move "simultaneously"
    # not technically simultaneous, but marginally closer to it than doing so without wait=True
    for i in range(minN,maxN):
        servos[i].move_start()

    # Sleep for enough time for motors to finish homing
    time.sleep(1.5)

# Handle servos timing out
except ServoTimeoutError as e:
    print(f"MOVE ERROR: Servo {e.id_} is not responding. Exiting...")
    quit()

freq=2*np.pi
# freq = 1
# freq=np.pi

# a=10, b=15 kind of works... kind of
a = 10
b = 15

t = 0

move_time = 100

# while True:
for j in range(100):
    try:
        # # Listing out explicitly while I figure it out
        # # This one it slips and doesn't really push forward at all
        servos[1].move(np.sin(freq*t)*a + 120, time=move_time)
        servos[2].move(np.cos(freq*t)*b + 75, time=move_time)

        servos[3].move(np.cos(freq*t)*a + 177, time=move_time)
        servos[4].move(np.sin(freq*t)*b + 73, time=move_time)

        servos[5].move(np.cos(freq*t)*a + 120, time=move_time)
        servos[6].move(np.sin(freq*t)*b + 126, time=move_time)

        servos[7].move(np.sin(freq*t)*a + 170, time=move_time)
        servos[8].move(np.cos(freq*t)*b + 90, time=move_time)

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
    time.sleep(0.1)
    # time.sleep(0.1) # combining with move_time effectively slows down the movement without jitters 
    # but it is much less stable when time sleep is 0.1 

