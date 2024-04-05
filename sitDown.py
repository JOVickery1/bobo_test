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
        servos[i].set_angle_limits(0, 240)
        servos[i].enable_torque()

except ServoTimeoutError as e:
    print(f"INITIALIZATION ERROR: Servo {e.id_} is not responding. Exiting...")
    quit()

# error_count = 0
# while True:
#     try:
#         for i in range(minN,maxN):
#             print(f'Servo {i}: {servos[i].get_physical_angle()}')
#     except ServoTimeoutError as e:
#         error_count+=1
#         if error_count == 5:
#             print(f'Quitting because of servo {e.id_}')
#             quit()
#         continue
#     break

targetAngles = np.array([0., 99.36, 0, 154.8, 0, 99.84, 40, 153.84, 7.44])

try:
    # Iterate through motors 1 to 8
    for i in range(5, maxN):
        # Move to target angle over 1 second
        if i == 6:
            servos[i].move(targetAngles[i],time=1250)
        else: 
            servos[i].move(targetAngles[i], time = 1000)
        # time.sleep(0.05)
    time.sleep(0.25)
    for i in range(minN,6):
        servos[i].move(targetAngles[i], time = 1000)
        # time.sleep(0.05)
except ServoTimeoutError as e:
    print(f"MOVE ERROR: Servo {e.id_} is not responding. Exiting...")
    quit()


'''Why doesn't it disable torques????'''
# time.sleep(1.5)
# for i in range(minN, maxN):
#     servos[i].disable_torque
# for i in range(minN, maxN):
#     errors_counter = 0
#     while True:
#         try:
#             servos[i].disable_torque
#         except ServoTimeoutError as e:
#             if errors_counter == 5:
#                 errors_counter+=1
#                 print(f'Error on servo {e.id_}. Quitting...')
#                 quit()
#             continue
#         break
