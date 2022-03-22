use linux_embedded_hal::I2cdev;

fn main() {
    println!("Creating I2C-1 device.");
    let mut dev = I2cdev::linux::I2CDevice::new("/dev/i2c-1").unwrap();
    dev.set_slave_address(0x2C);
    dev.write(0xF32D);
    let read_buff = vec![0; 3];
    dev.read().unwrap();
    println!("Buffer: {}", read_buff)
}
