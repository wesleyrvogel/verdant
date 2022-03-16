"""
This contains the top-level control loop for the hydroponics 
setup.
"""
import system_interface
import time
import RPi.GPIO as gpio


# Inital resource setup
print('Setting up hardware resource allocation.')
gpio.setmode(gpio.BOARD)  # This sets pin addressing scheme
big_pump = system_interface.GPIOController(37)  # This is the main water pump

for i in range(3):
    print('Turning pump on!')
    big_pump.set_state(True)
    time.sleep(2)
    print('Turning pump off!')
    big_pump.set_state(False)
    time.sleep(2)

# Functional control loop
errored = True  # Set to true to skip the loop during dev

print('Starting control loop.')
while not errored:
    try:
        # Collect sensor measurements

        # Determine what hardware needs to be actuated

        # Wait until next control period
        time.sleep(10)  # Sleep in s, so ~10s period
    except Exception as ex:
        print(ex)

# Resource deallocation
print('Performing resource cleanup.')
gpio.cleanup()  # This cleans up the GPIO resources
