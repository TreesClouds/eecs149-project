from machine import UART, Pin, I2C, time_pulse_us
from pololu_3pi_2040_robot import robot
import time
from time import sleep_us, sleep

# Initialize UART for HM-10 communication
uart = UART(0, baudrate=9600, tx=Pin(28), rx=Pin(29))

# Initialize motors and variables
motors = robot.Motors()
speed = motors.MAX_SPEED * 0.15

# Define ultrasonic pins
TRIGGER_PIN = 24 # Shared trigger pin (GP24)
ECHO_PIN1 = 26   # Echo pin for sensor 1 (GP26) front expansion
ECHO_PIN2 = 20    # Echo pin for sensor 2 (GP20) front expansion
ECHO_PIN3 = 27    # Echo pin for sensor 3 (GP27) mid expansion

# Set up ultrasonic pins
trigger = Pin(TRIGGER_PIN, Pin.OUT)
echo1 = Pin(ECHO_PIN1, Pin.IN)
echo2 = Pin(ECHO_PIN2, Pin.IN)
echo3 = Pin(ECHO_PIN3, Pin.IN)

# Ultrasonic variables
distance1 = 'None' # Left
distance2 = 'None' # Right
distance3 = 'None' # Forward

# Initialize IMU
imu = robot.IMU()
imu.reset()
imu.enable_default()


def send_data(command):
    uart.write(command + '\r\n')



#time to wait before measuring again
measure_wait_time = 500
last_measure = 0

#initialize gyro variables
last_time_gyro_reading = None
turn_rate = 0.0     # degrees per second
robot_angle = 0.0   # degrees
target_angle = 0.0
last_time_gyro_reading = None
angle_to_turn = 90
change_dir = 180
direction = "right"

#variables for setting turn speed:
max_speed = 3000
kp = 140
kd = 4


#measure distance
def measure_distance():
    trigger.low()
    sleep_us(2)
    trigger.high()
    sleep_us(10)
    trigger.low()
    duration1 = time_pulse_us(echo1, 1, 30000)  # 30ms timeout
    if duration1 < 0:
        distance1 = 'None'
    else:
        distance1 = (duration1 * 0.0343) / 2
    
    trigger.low()
    sleep_us(2)
    trigger.high()
    sleep_us(10)
    trigger.low()
    duration2 = time_pulse_us(echo2, 1, 30000)  # 30ms timeout
    if duration2 < 0:
        distance2 = 'None'
    else:
        distance2 = (duration2 * 0.0343) / 2

    trigger.low()
    sleep_us(2)
    trigger.high()
    sleep_us(10)
    trigger.low()
    duration3 = time_pulse_us(echo3, 1, 30000)  # 30ms timeout
    if duration3 < 0:
        distance3 = 'None'
    else:
        distance3 = (duration3 * 0.0343) / 2

    return None

# Turn @param: direction. @values +/-90, 180. @return void
def turn(direction):
    global target_angle, last_time_gyro_reading
    global robot_angle, turn_rate
    target_angle = robot_angle + direction
    while True:
        if imu.gyro.data_ready():
            imu.gyro.read()
            turn_rate = imu.gyro.last_reading_dps[2]  # degrees per second
            now = time.ticks_us()
        if last_time_gyro_reading:
            dt = time.ticks_diff(now, last_time_gyro_reading)
            robot_angle += turn_rate * dt / 1000000
        last_time_gyro_reading = now
        
        far_from_target = abs(robot_angle - target_angle) > 3
        if far_from_target:
            turn_speed = (target_angle - robot_angle) * kp - turn_rate * kd
            if turn_speed > max_speed: turn_speed = max_speed
            if turn_speed < -max_speed: turn_speed = -max_speed
            
            motors.set_speeds(-turn_speed, turn_speed)
            last_time_far_from_target = time.ticks_ms()
        else:
            motors.off()
            break
    return None            

# def pid(error, p=1, i=0, d=0):
#     global integral, last_error
#     integral = integral + error
#     derivative = error - last_error
#     output = p * error + i * integral + d * derivative
#     last_error = error
#     return output

# # TODO: Add to loop
# # This function assumes the ultrasonic code above is working & looping
# def control_timestep():
#     if distance3 < 10: # If wall in front of robot, stop
#         motors.set_speeds(0, 0)
#     if distance1 and distance2: # If walls on both sides of robot, move straight with PID control
#         error = (distance1 - distance2) / 2
#         correction = pid(error, p=1, i=0, d=0)
#         motors.set_speeds(speed - correction, speed + correction)
#     else: # Otherwise, just move straight
#         motors.set_speeds(speed, speed)

        


while True:
    if ((time.time_ns()/1000000) - last_measure) >= measure_wait_time:
        measure_distance()
        last_measure = time.time_ns()/1000000
        send_data(f'distance1: {distance1}')
        send_data(f'distance2: {distance2}')
        send_data(f'distance3: {distance3}')
        send_data(f'direction: {direction}')
    if distance1 != 'None':
        motors.set_speeds(0,0)
    if uart.any():
        data = uart.read(1).decode()     
        if direction == "right":
            if data == 'r':
                send_data('forward')
                motors.set_speeds(speed, speed)             
            elif data == 'l':
                send_data('turning 180')
                direction = "left"
                turn(change_dir)
            elif data == 'u':
                send_data('turning left')
                direction = "up"
                turn(angle_to_turn)
            elif data == 'd':            
                send_data('turning right')
                direction = "down"
                turn(-angle_to_turn)
        
        elif direction == "left":
            if data == 'l':
                send_data('forward')
                motors.set_speeds(speed, speed)
            elif data == 'r':
                send_data('turning 180')
                direction = "right"
                turn(change_dir)
            elif data == 'd':
                send_data('turning right')
                direction = "down"
                turn(angle_to_turn)
            elif data == 'u':            
                send_data('turning left')
                direction = "up"
                turn(-angle_to_turn)
        
        elif direction == "up":
            if data == 'u':
                send_data('forward')
                motors.set_speeds(speed, speed)
            elif data == 'd':
                send_data('turning 180')
                direction = "down"
                turn(change_dir)
            elif data == 'r':
                send_data('turning right')
                direction = "right"
                turn(-angle_to_turn)
            elif data == 'l':            
                send_data('turning left')
                direction = "left"
                turn(angle_to_turn)
        
        elif direction == "down":
            if data == 'd':
                send_data('forward')
                motors.set_speeds(speed, speed)
            elif data == 'u':
                send_data('turning 180')
                direction = "up"
                turn(change_dir)
            elif data == 'l':
                send_data('turning right')
                direction = "left"
                turn(-angle_to_turn)
            elif data == 'r':            
                send_data('turning left')
                direction = "right"
                turn(angle_to_turn)

        