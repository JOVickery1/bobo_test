from math import sin, cos
from lx16a import *
import time

LX16A.initialize("/dev/ttyUSB0", 0.1)

try:
    #servo1 = LX16A(1)
    #servo2 = LX16A(2)
    servo3 = LX16A(3)
    servo4 = LX16A(4)
    servo5 = LX16A(5)
    servo6 = LX16A(6)
    servo7 = LX16A(7)
    servo8 = LX16A(8)
    #servo1.set_angle_limits(0, 240)
    #servo2.set_angle_limits(0, 240)
    servo3.set_angle_limits(0, 240)
    servo4.set_angle_limits(0, 240)
    servo5.set_angle_limits(0, 240)
    servo6.set_angle_limits(0, 240)
    servo7.set_angle_limits(0, 240)
    servo8.set_angle_limits(0, 240)
    #servo1Angle = servo1.get_physical_angle()
    #servo2Angle = servo2.get_physical_angle()
    #print(f'servo 1 angle {servo1Angle}')
    #print(f'servo 2 angle {servo2Angle}')
except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

t = 0
while True:
#    servo1.move(sin(t) * 10 + 120)
#    servo2.move(cos(t) * 60 + 60)

    #servo1.move(120)
    #servo2.move(65)
    
    servo3.move(150)
    servo4.move(65)
    
    servo5.move(150)
    servo6.move(65)
    
    servo7.move(150)
    servo8.move(65)

    time.sleep(0.05)
    t += 0.1
