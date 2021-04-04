# Diagon-Alley

Everything a young witch or wizard needs to get themselves set up.

## Google Service Installation

**This does need setting up as a google service account, your google calendars shared with this account, etc. I'll put instructions here.**

## Raspberry Pi Setup

1) Download and install the [Raspberry Pi Imager](https://www.raspberrypi.org/software/).
1) Write `Raspberry Pi OS Lite` to an SD card, do not boot just yet.
1) Set up the [Pi for wireless](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md).
1) Set up [SSH for headless](https://www.raspberrypi.org/documentation/remote-access/ssh/README.md).
1) Put the SD card in the Pi and boot.
1) Some generic initial setup tasks, via `ssh pi@raspberrypi.local`
	* `raspi-config` to adjust password
	* `raspi-config` to adjust hostname
	* `sudo apt-get update -y`
	* `sudo apt-get install python3-pip -y`  
	* `sudo apt-get upgrade -y`
1) Some IoT setup tasks, still via `ssh pi@raspberrypi.local`
	* We will be using an `iot` account to execute our code, and the `pi` account if we need terminal access.
	* `sudo adduser iot`
	* `sudo adduser iot sudo`
	* `su - iot` to switch to the new user
	* `sudo raspi-config` to configure auto-login
1) Reboot, `sudo reboot`

## Application Installation

1) Create a folder for the code, `ssh iot@<hostname>.local 'mkdir /home/iot/src'`
1) Copy the application code, `scp -r ./* iot@<hostname>.local:/home/iot/src`
1) Install the dependencies
	* `ssh iot@<hostname>.local 'sudo pip3 install -r src/diagon_alley/pi_requirements.txt'`
1) Start the program on login
	1) `ssh iot@<hostname>.local`
	1) `sudo nano /home/iot/.bashrc`
	1) Add `cd /home/iot/src` as the final line
	1) Add `sudo python3 main.py <led_count> <calendar> ... <calendar>` as the final line
	1) Save and close
	1) `sudo visudo`
	1) Add `iot ALL = NOPASSWD: /usr/bin/python3` as the final line
	1) Save, close and reboot
