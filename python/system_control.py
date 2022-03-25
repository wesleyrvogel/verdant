"""
This contains the top-level control loop for the hydroponics 
setup.
"""
import system_interface
from system_interface import ADS1115Range
import time
import RPi.GPIO as gpio


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

# This is the ADC
adc = system_interface.ADCController()
adc.set_full_scale_range(ADS1115Range.Range6_144V)

# This is a little state logger
logger = system_interface.StateLogger('/home/pi/verdant_logs/')

# First, let's safe the system
set_safe_state()

# Functional control loop
errored = False  # Set to true to skip the loop during dev

print('Starting control loop.')

# Valve on!
valve_open.set_state(True)
time.sleep(.7)  # 700ms is approximately the minimum flow rate
valve_open.set_state(False)

while not errored:
    try:
        # Collect sensor measurements
        # It takes 1s to read conductivity right now
        conductivity = conductivity_sensor.get_conductivity()
        co2 = co2_sensor.get_co2_concentration()
        ph = adc.get_channel_reading(0)
        logger.log_values(co2, conductivity)

        # Determine what hardware needs to be actuated
        print('Conductivity: {} us/cm'.format(conductivity))
        print('pH Raw Reading: {} V'.format(ph))
        # Fresh water has conductivity around 10-30 us/cm
        # Pure salt water has closer to 15000 or more us/cm
        # Plants like around 800-1200 us/cm
        # The Base A/ Base B liquids are EXTREMELY conductive,
        # like off the charts unreadable conductive.
        if conductivity < 900:
            print('Pump on to increase conductivity')
            peristaltics[0].set_state(True)
            time.sleep(5)
            peristaltics[0].set_state(False)

        # Wait until next control period
        time.sleep(.1)  # Sleep for the loop here 
    except (Exception, KeyboardInterrupt) as ex:
        set_safe_state()
        gpio.cleanup()
        conductivity_sensor.close_connection()
        print(ex)
        errored = True

#Attempting to safe system
set_safe_state()

# Resource deallocation
print('Performing resource cleanup.')
gpio.cleanup()  # This cleans up the GPIO resources
conductivity_sensor.close_connection()
