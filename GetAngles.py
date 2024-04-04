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
        servos[i].disable_torque

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

realAngles = np.array([0]*9, dtype='f')

desiredAngles = np.array([0]*9, dtype='f')

for i in range(minN, maxN):
    if i % 2 == 1:
        desiredAngles[i] = 150
    else:
        desiredAngles[i] = 70

while True:
    try:
        # Iterate through motors 1 to 8
        for i in range(minN, maxN):
            realAngles[i] = servos[i].get_physical_angle()
            print(f'Servo {i} has angle {realAngles[i]}')
        print(realAngles)
        print()

    except ServoTimeoutError as e:
        print(f"Servo {e.id_} is not responding. Exiting...")
        quit()
    time.sleep(1)