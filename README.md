# Python nRF51 DFU Server

A python script for bluez gatttool using pexpect to achive Device Firmware Updates (DFU) to the nRF51.  
The host system is assumed to be some flavor of Linux.

## Prerequisite

* sudo pip install pexpect
* sudo pip install intelhex
* [Bluez](https://learn.adafruit.com/pibeacon-ibeacon-with-a-raspberry-pi/setting-up-the-pi "BlueZ build")

## Firmware Build Requirement
* Your nRF51 firmware build method will produce either a firmware hex or bin file named *application.hex* or *application.bin*.  This naming convention is per Nordics DFU specification, which is use by this DFU server as well as the Android Master Control Panel DFU, and iOS DFU app.  
* Your nRF51 firmware build method will produce an Init file (aka *application.dat*).  Again, this is per Nordic's naming conventions.

## Usage

```
sudo ./dfu.py -z ~/application.zip -a EF:FF:D2:92:9C:2A
```

To figure out the address of DfuTarg do a 'hcitool lescan' -

```
$ sudo hcitool -i hci0 lescan  
LE Scan ...   
CD:E3:4A:47:1C:E4 DfuTarg  
CD:E3:4A:47:1C:E4 (unknown)
```
