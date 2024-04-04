from lx16a import *
import time
import numpy as np

LX16A.initialize("/dev/ttyUSB0", 0.1)

minN = 1
maxN = 9

servos = [0]
angles = [0]

try:
    for i in range(minN, maxN):
        servos.append(LX16A(i))
        angles.append(servos[i].get_physical_angle())

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

for i in range(minN, maxN):
    print(f'Servo {i} is at {int(angles[i])} degrees')