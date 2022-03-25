import system_interface
from system_interface import ADS1115Range
import RPi.GPIO as gpio
import time


# GPIO Test
print('Testing GPIO control.')
gpio.setmode(gpio.BOARD)  # This sets pin addressing scheme
peristaltics = []
for pin in [37, 35, 33, 31]:
    peristaltics.append(system_interface.GPIOController(pin))

valve_open = system_interface.GPIOController(29)
valve_close = system_interface.GPIOController(32)

"""
for period in [0.1, 0.5, 1, 1.5, 2]:
    peristaltics[0].set_state(True)
    time.sleep(period)
    peristaltics[0].set_state(False)
    time.sleep(5)
"""

for pump in peristaltics:
    pump.set_state(True)
    time.sleep(3)
    pump.set_state(False)

valve_open.set_state(True)
time.sleep(4)
valve_open.set_state(False)
valve_close.set_state(True)
time.sleep(4)
valve_close.set_state(False)

for pump in peristaltics:
    pump.set_state(True)

time.sleep(5)

for pump in peristaltics:
    pump.set_state(False)

print('Performing GPIO cleanup.')
gpio.cleanup()  # This cleans up the GPIO resources

# Conductivity sensor test
print('Testing conductivity sensor.')
conductivity_sensor = system_interface.ConductivitySensor('/dev/serial0')
for i in range(3):
    conductivity = conductivity_sensor.get_conductivity()
    print('Approximate liquid conductivity: {} us/cm'.format(conductivity))
    time.sleep(1)

# CO2 Test
print('Testing CO2 sensor.')
co2_sensor = system_interface.CO2Sensor()
co2_ppm = co2_sensor.get_co2_concentration()
print('Approximate CO2 PPM: {}'.format(co2_ppm))

# ADC Test
print('Testing ADC connection.')
adc = system_interface.ADCController()
adc.set_full_scale_range(ADS1115Range.Range6_144V)
for i in range(4):
    reading = adc.get_channel_reading(i)
    print('Channel {} reading: {}'.format(i, reading))

