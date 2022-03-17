import system_interface
from system_interface import ADS1115Range
import RPi.GPIO as gpio
import time


# GPIO Test
print('Testing GPIO control.')
gpio.setmode(gpio.BOARD)  # This sets pin addressing scheme
big_pump = system_interface.GPIOController(37)  # This is the main water pump

big_pump.set_state(True)
time.sleep(1)
print('GPIO 37 on.')
big_pump.set_state(False)
time.sleep(1)
print('GPIO 37 off.')

print('Performing GPIO cleanup.')
gpio.cleanup()  # This cleans up the GPIO resources

# CO2 Test
print('Testing CO2 sensor.')
co2_sensor = system_interface.CO2Sensor()
co2_ppm = co2_sensor.get_co2_concentration()
print('Approximate CO2 PPM: {}'.format(co2_ppm))

# ADC Test
print('Testing ADC connection.')
adc = system_interface.ADCController()
adc.set_full_scale_range(ADS1115Range.6_144V)
for i in range(4):
    reading = adc.get_channel_reading(i)
    print('Channel {} reading: {}'.format)

