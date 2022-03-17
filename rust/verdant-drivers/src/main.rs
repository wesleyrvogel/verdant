use embedded_hal::adc::OneShot;
use linux_embedded_hal::I2cdev;
use nb::block;
use std::env;
use ads1x1x::{channel, Ads1x1x, SlaveAddr, FullScaleRange};

fn main() {
    // First, let's instantiate the device
    let dev = I2cdev::new("/dev/i2c-2").unwrap();
    let address = SlaveAddr::default();
    let mut adc = Ads1x1x::new_ads1115(dev, address);

    // Then, let's get the command line args that specify 
    // what channel and range to use
    let args: Vec<String> = env::args().collect();
    let chan: usize = args[1].parse().unwrap();  // Desired channel to read
    let range: usize = args[2].parse().unwrap();  // Desired range to use

    // Let's set the full scale range as specified
    let ranges = [
        FullScaleRange::Within0_256V,
        FullScaleRange::Within0_512V,
        FullScaleRange::Within1_024V,
        FullScaleRange::Within2_048V,
        FullScaleRange::Within4_096V,
        FullScaleRange::Within6_144V
    ];
    let range_values = [
        0.256,
        0.512,
        1.024,
        2.048,
        4.096,
        6.144
    ];
    adc.set_full_scale_range(ranges[range]).unwrap();

    // Then, let's read the value that we want
    let value: f32 = match chan {
        0 => block!(adc.read(&mut channel::SingleA0)).unwrap().into(),
        1 => block!(adc.read(&mut channel::SingleA1)).unwrap().into(),
        2 => block!(adc.read(&mut channel::SingleA2)).unwrap().into(),
        3 => block!(adc.read(&mut channel::SingleA3)).unwrap().into(),
        _ => 0.0
    };

    // Then let's get the voltage from the measured counts
    // This is a 16-bit ADC, so we use 2^16 in the denominator
    let voltage: f32 = value / 32768.0 * range_values[range];

    println!("{}", voltage);
    
    // Let's clean up after ourselves
    let _dev = adc.destroy_ads1115();
}
