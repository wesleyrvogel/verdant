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

# These are the four peristaltic pumps
### ADD THESE WHEN HARDWARE IS ALLOCATED ###

# This is the conductivity sensor
conductivity_sensor = system_interface.ConductivitySensor('/dev/serial0')

# This is the CO2 sensor
co2_sensor = system_interface.CO2Sensor()

# This is a little state logger
logger = system_interface.StateLogger('/home/pi/verdant_logs/')

# Functional control loop
errored = False  # Set to true to skip the loop during dev

print('Starting control loop.')
while not errored:
    try:
        # Collect sensor measurements
        conductivity = conductivity_sensor.get_conductivity()
        co2 = co2_sensor.get_co2_concentration()
        logger.log_values(co2, conductivity)

        # Determine what hardware needs to be actuated

        # Wait until next control period
        time.sleep(10)  # Sleep in s, so ~10s period
    except Exception as ex:
        print(ex)
        errored = True

# Resource deallocation
print('Performing resource cleanup.')
gpio.cleanup()  # This cleans up the GPIO resources
conductivity_sensor.close_connection()
