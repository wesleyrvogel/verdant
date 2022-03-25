"""
This contains the top-level control loop for the hydroponics 
setup.
"""
import system_interface
import time
import RPi.GPIO as gpio
import IPython

# Inital resource setup
print('Setting up hardware resource allocation.')
gpio.setmode(gpio.BOARD)  # This sets pin addressing scheme

# Let's create controllers for the peristaltic pumps
peristaltics = []
for pin in [37, 35, 33, 31]:
    peristaltics.append(system_interface.GPIOController(pin))

# And one more for the controllable valve interface
valve_open = system_interface.GPIOController(29)
valve_close = system_interface.GPIOController(32)

def set_safe_state():
    # First, turn off all peristaltic pumps
    for pump in peristaltics:
        pump.set_state(False)

    # Then, close the valuve fully
    valve_open.set_state(False)
    valve_close.set_state(True)
    time.sleep(6)
    valve_close.set_state(False)

# This is the conductivity sensor
conductivity_sensor = system_interface.ConductivitySensor('/dev/serial0')

# This is the CO2 sensor
co2_sensor = system_interface.CO2Sensor()

IPython.embed()
