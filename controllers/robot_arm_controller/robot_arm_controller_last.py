from controller import Robot
from controller import PositionSensor
import pygame

# get the time step of the current world.
timestep = 64
velocity = 0.2
F = 2.0   # frequency 2 Hz
t = 0.0   # elapsed simulation time

# create the Robot instance.
robot = Robot()

# Initialize the joysticks.
pygame.init()
pygame.joystick.init()

motor_1_pos_now = 0.0;
motor_1_auto_move_right = False;
motor_1_auto_move_left = False;

motors = [robot.getDevice('motor_1'), robot.getDevice('motor_2'), robot.getDevice('motor_3'), robot.getDevice('motor_4'), robot.getDevice('motor_5'), robot.getDevice('motor_6')]
pos_motors = [robot.getDevice('motor_1_s'), robot.getDevice('motor_2_s'), robot.getDevice('motor_3_s'), robot.getDevice('motor_4_s'), robot.getDevice('motor_5_s'), robot.getDevice('motor_6_s')]
axis = [None]*6
button = [None]*11

for motor in motors:
    motor.setPosition(float('inf'))
    motor.setVelocity(0.0) 

for pos_motor in pos_motors:
    pos_motor.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    pygame.event.get()
            
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        
        
        axes = joystick.get_numaxes()
        for i in range(axes):
            axis[i] = joystick.get_axis(i)
        
        buttons = joystick.get_numbuttons()
        for i in range(buttons):
            button[i] = joystick.get_button(i)
        
        # direction 9
        if axis[0] < -0.5:
            motors[0].setVelocity(velocity)
        # direction 11
        elif axis[0] > 0.5:
            motors[0].setVelocity(velocity*-1)
        
        # direction 8
        elif axis[1] < -0.5:
            motors[1].setVelocity(velocity*-1) 
        # direction 10
        elif axis[1] > 0.5:
            motors[1].setVelocity(velocity)
        
        # direction 7
        elif axis[3] < -0.5:
            motors[2].setVelocity(velocity) 
        # direction 5
        elif axis[3] > 0.5:
            motors[2].setVelocity(velocity*-1)
        
        # direction 4
        elif axis[4] < -0.5:
            motors[3].setVelocity(velocity) 
        # direction 6
        elif axis[4] > 0.5:
            motors[3].setVelocity(velocity*-1)
        
        elif button[4] == 1:
            motors[4].setVelocity(velocity*-1) 
        elif axis[2] > 0.5:
            motors[4].setVelocity(velocity)
        
        elif button[5] == 1:
            motors[5].setVelocity(velocity) 
        elif axis[5] > 0.5:
            motors[5].setVelocity(velocity*-1)
        
        elif button[9] == 1:
            motor_1_auto_move_left = True;
            motor_1_pos_now = pos_motors[0].getValue()
        elif button[10] == 1:
            motor_1_auto_move_right = True;
            motor_1_pos_now = pos_motors[0].getValue()
        else :
            # if motor_1_auto_move_right or motor_1_auto_move_left:
                # for i in range(1,6):
                    # motors[i].setVelocity(0.0)
            # else:
            for motor in motors:
                motor.setVelocity(0.0)
    
        if motor_1_auto_move_right:
            if pos_motors[0].getValue() > motor_1_pos_now - 1.57:
                motors[0].setVelocity(velocity*-1)
            else:
                motor_1_auto_move_right = False
        elif motor_1_auto_move_left:
            if pos_motors[0].getValue() < motor_1_pos_now + 1.57:
                motors[0].setVelocity(velocity)
            else:
                motor_1_auto_move_left = False  
        
pygame.quit()
 
