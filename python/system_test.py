import system_interface
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
