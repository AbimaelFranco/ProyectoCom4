import pygame
from time import sleep

# Initialize pygame
pygame.init()

# Set up the joystick
pygame.joystick.init()

# Check for joystick presence
if pygame.joystick.get_count() == 0:
    print("No joystick detected.")
    exit()
else:
    print(f"Detected {pygame.joystick.get_count()} joystick(s).")

# Initialize the first joystick
try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Joystick initialized successfully.")
    print(f"Joystick name: {joystick.get_name()}")
    print(f"Number of axes: {joystick.get_numaxes()}")
    print(f"Number of buttons: {joystick.get_numbuttons()}")
    print(f"Number of hats: {joystick.get_numhats()}")
except pygame.error:
    print("Failed to initialize joystick.")
    exit()

# Store previous axis values to detect changes
previous_axis_values = [0] * joystick.get_numaxes()

# Store previous button states to detect changes
previous_button_states = [0] * joystick.get_numbuttons()

# Store previous hat states to detect changes
previous_hat_states = [0] * joystick.get_numhats()

axis_counters = [0] * joystick.get_numaxes()
hat_counters = [0] * joystick.get_numhats()

def update_counter(counter, value):
    new_counter = counter + value
    return max(-90, min(90, new_counter))

try:
    while True:
        # Process pygame events
        pygame.event.pump()

        # Loop through all axes and print value if it changes
        for i in range(joystick.get_numaxes()):
            axis_value = joystick.get_axis(i)
            if abs(axis_value) > 0.01:
                if i != 5:
                    if i!= 2:
                        counter_increment = axis_value
                        axis_counters[i] = update_counter(axis_counters[i], counter_increment)
                        print(f"Axis {i} value: {axis_value}, Counter: {axis_counters[i]}")
                previous_axis_values[i] = axis_value
            
            # if abs(axis_value - previous_axis_values[i]) > 0.01:  # Threshold to detect change
            #     print(f"Axis {i} value: {axis_value}")
            #     previous_axis_values[i] = axis_value

        # Loop through all buttons and print value if it changes
        for i in range(joystick.get_numbuttons()):
            button_state = joystick.get_button(i)
            if button_state != previous_button_states[i]:
                print(f"Button {i} {'pressed' if button_state else 'released'}")    #Return int 0 or 1
                previous_button_states[i] = button_state
                if i == 7 and button_state == 1:
                    print("Saliendo............................")

        # Loop through all hats (d-pads) and print value if it changes
        for i in range(joystick.get_numhats()):
            hat_state = joystick.get_hat(i)
            # if hat_state != previous_hat_states[i]:
            #     print(f"Hat {i} value: {hat_state}")
            #     previous_hat_states[i] = hat_state
            if hat_state != (0, 0):  # If hat is not centered
                if hat_state[0] != 0:  # Horizontal direction
                    counter_increment = hat_state[0] * 0.1  # Increment proportional to time
                    hat_counters[i] = update_counter(hat_counters[i], counter_increment)
                if hat_state[1] != 0:  # Vertical direction
                    counter_increment = hat_state[1] * 0.1  # Increment proportional to time
                    hat_counters[i] = update_counter(hat_counters[i], counter_increment)
                print(f"Hat {i} value: {hat_state}, Counter: {hat_counters[i]}")
            previous_hat_states[i] = hat_state

        # Add a small delay to reduce CPU usage
        sleep(0.1)

except KeyboardInterrupt:
    # Graceful exit
    print("Exiting...")
finally:
    # Clean up
    pygame.quit()
