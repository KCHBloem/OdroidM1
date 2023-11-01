# OdroidM1 for Lager Testbank
This Repository will contain the instructions for installing the operating system on the Odroid M1 single board computer that is in charge of controlling the lager testbank for the HVA.
The repository will also contain the python code necessary to read the sensor data from the lager testbank and it will contain the react web dashboard project.

### Operating System:
Version: `Ubuntu 22.04.01 Desktop` or `Debian 12 (Bookworm)`

Username: `odroid`

Password: `odroid`

IP: _Can be found under network settings on the device._

#### Ubuntu:
Image: [Github Page](https://github.com/TheRemote/Legendary-ODROID-M1)
1. Flash the image onto an SD card using something like [Balena Etcher](https://etcher.balena.io)
2. Insert the SD card into the SD card slot on the M1 and power on the device
3. On boot you should first enter the petitboot OS, from here you can select the disk that ubuntu is installed on and boot from there

#### Debian: 
1. Boot the Odroid M1 and navigate to "Exit to shell"
2. Enter: `uhdcpc`
3. Enter: `exit`
4. Select Debian 12 at the top and follow the installation


### Required Packages and Software (Internet Connection Required)
Start of by running: `sudo apt update` and `sudo apt install python3 python3-pip`. If you get an error about not being able to connect to the ubuntu servers try to create a static ip address and changing the DNS server.
Then install the following dependencies:
- Firefox: `sudo snap install firefox`
- WiringPi: `sudo python3 -m pip install odroid-wiringpi` and `sudo apt install odroid-wiringpi`
- Spidev: `sudo python3 -m pip install spidev`

### Code Example Wiring Pi
Use `sudo gpio readall` to see pinout [More Info](https://wiki.odroid.com/odroid-m1/application_note/gpio/wiringpi#tab__github_repository1)
```python
#!/usr/bin/env python
 
import odroid_wiringpi as wpi
import time
 
wpi.wiringPiSetup()
wpi.pinMode(0, 1)
 
while True:
    wpi.digitalWrite(0, 1)
    time.sleep(1)
    wpi.digitalWrite(0, 0)
    time.sleep(1)
```


### SPI Installation (might not be required)
Open config.ini in the boot directory using: `sudo nano /boot/config.ini`

It should look something like this:
```
[generic]
overlay_resize=16384
overlay_profile=
overlays="i2c0 i2c1 spi0"

[overlay_custom]
overlays="i2c0 i2c1"

[overlay_hktft32]
overlays="hktft32 ads7846"
```

Edit it to look like this (add the last part):
```
[generic]
overlay_resize=16384
overlay_profile=
overlays="i2c0 i2c1 spi0"

[overlay_custom]
overlays="i2c0 i2c1"

[overlay_hktft32]
overlays="hktft32 ads7846"

[overlay_spi]
overlays="spi0"
```
Then run `ls -al /dev/spi*` to see if spidev0.0 shows up. [More Info](https://wiki.odroid.com/common/application_note/gpio/enable_spi_i2c_uart_with_dtbo#tab__odroid-m11) [Even More Info](https://wiki.odroid.com/odroid-m1/application_note/gpio/spi#tab__odroid-m12)

