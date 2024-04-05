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

# Define goal angles for upper and lower motors
goalAngleUpper = 150
goalAngleLower = 65

# Create an array to store goal angles for each motor
goalAngle = [0]     # First value is set to 0 so that motor numbers and array indices line up

# Set odd numbered motors to goalAngleUpper and even to goalAngleLower
for i in range(minN, maxN):
    if i % 2 == 1:
        goalAngle.append(goalAngleUpper)
    else:
        goalAngle.append(goalAngleLower)

# print(goalAngle)

# Determined from measurement of bobo        
# goalAngle = [0, 121, 73, 161, 54, 123, 97, 161, 76]
# goalAngle = np.array([0, 119.76, 81.84, 176.88, 56.88, 118.56, 126, 171.36, 92.16])
        #                  1      2      3      4      5       6       7       8
goalAngle = np.array([0., 120., 74.88, 177.6, 73.44, 119.76, 126.48, 171.36, 90.72])

# Initialize first value of cur
currentAngle = [0]  # First value is set to 0 so that motor numbers and array indices line up

# Define boolean to determine if motors are moving
motorsMoving = False

# Define boolean for the first loop
firstRun = True

while True:
    errors_count = 0
    while True:
        try:
            # Iterate through motors 1 to 8
            for i in range(minN, maxN):
                if not motorsMoving:
                    # Get current physical angle
                    currentAngle.append(servos[i].get_physical_angle())

                    # Move motor to its goal angle
                    servos[i].move(goalAngle[i], wait=True, time = 1500)

                    # Print the currentAngle array once it is fully populated
                    if i == maxN:
                        print(currentAngle)
                else:
                    # If motors are already moving then overwrite currentAgnle rather than append
                    currentAngle[i] = servos[i].get_physical_angle()

            if firstRun:
                # Set motors to move "simultaneously"
                # not technically simultaneous, but marginally closer to it than doing so without wait=True
                for i in range(minN,maxN):
                    servos[i].move_start()

            # Set motors moving to true
            motorsMoving = True

        # Handle servos timing out
        except ServoTimeoutError as e:
            errors_count+=1
            print(f"MOVE ERROR: on Servo {e.id_} (responding)")
            if errors_count == 5:
                print(f"MOVE ERROR: Servo {e.id_} is not responding. Exiting...")
                quit()
            continue
            # quit()
        break

    # On first loop wait 1 second for motors to move to position
    if firstRun:
        time.sleep(1)
        firstRun = False

    # Initialize variable for counting the number of homed motors
    homed_motors = 0

    # Define flag for waiting (used later)
    waitForMove = False

    # Check if the motors are homed yet
    for i in range(minN, maxN):
        # Print how far each motor is from its goal
        # note this is error at the start of the while loop, not current error at execution time
        # print(f'Servo {i} Angle Error: {abs(currentAngle[i] - goalAngle[i])}')

        # Check if motor is at goal angle, if so add 1 to homed_motors
        if abs(currentAngle[i] - goalAngle[i]) <= 2:
            homed_motors += 1
        else:
            # Send a new move command
            # servos[i].move(goalAngle[i], time = 250)
            # Flag the program to wait for this motor to finish moving before looping
            waitForMove = True

    # Carriage return for viewing motor errors output easily.
    print()

    # If all eight motors are homed, disable torques for each motor and end program
    if homed_motors == 8:
        for i in range(minN, maxN):
            try:
                servos[i].disable_torque()
                # print(f'torque on motor {i} disabled')
                print(servos[i].is_torque_enabled())
            except ServoTimeoutError as e:
                print(f'Error with servo {e.id}')
                pass
        # print('Right before quit:')
        # for i in range(minN,maxN):
        #     print(servos[i].is_torque_enabled())  
        break
        # quit()