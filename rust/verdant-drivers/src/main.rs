use embedded_hal::adc::OneShot;
use linux_embedded_hal::I2cdev;
use nb::block;

use ads1x1x::{channel, Ads1x1x, SlaveAddr};

fn main() {
    // First, let's instantiate the device
    let dev = I2cdev::new("/dev/i2c-2").unwrap();
    let address = SlaveAddr::default();
    let mut adc = Ads1x1x::new_ads1115(dev, address);

    // Then, let's read all of the values
    let values = [
        block!(adc.read(&mut channel::SingleA0)).unwrap(),
        block!(adc.read(&mut channel::SingleA1)).unwrap(),
        block!(adc.read(&mut channel::SingleA2)).unwrap(),
        block!(adc.read(&mut channel::SingleA3)).unwrap(),
    ];
    for (channel, value) in values.iter().enumerate() {
        println!("Channel {}: {}", channel, value);
    }
    
    // Let's clean up after ourselves here
    let _dev = adc.destroy_ads1115();
}
