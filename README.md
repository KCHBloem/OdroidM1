# OdroidM1 for Lager Testbank
This Repository will contain the instructions for installing the operating system on the Odroid M1 single board computer that is in charge of controlling the lager testbank for the HVA.
The repository will also contain the python code necessary to read the sensor data from the lager testbank and it will contain the react web dashboard project.

### Operating System:
Version: `Ubuntu 22.04.01 Desktop`
Username: `odroid`
Password: `odroid`

Image: [Github Page](https://github.com/TheRemote/Legendary-ODROID-M1)
1. Flash the image onto an SD card using something like [Balena Etcher](https://etcher.balena.io)
2. Insert the SD card into the SD card slot on the M1 and power on the device
3. On boot you should first enter the petitboot OS, from here you can select the disk that ubuntu is installed on and boot from there

### Required Packages and Software (Internet Connection Required)

- Firefox: `sudo snap install firefox`
- WiringPi: ``

