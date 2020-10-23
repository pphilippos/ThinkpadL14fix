#!/bin/env python

# Notes:
# - Must be run as root, if not as a service (see note below)
# - thinkpad_acpi must be enabled
# - /etc/modprobe.d/thinkpad_acpi.conf must contain "options thinkpad_acpi fan_control=1"
# - The fan level function may be different from laptop to laptop
# - For a systemd startup service, I used the following script at file "/lib/systemd/system/l14fix.service"

'''
[Unit]
Description=Thinkpad L14 fix script Philippos
After=multi-user.target[Service]

[Service]
Type=idle
User=root
ExecStart=/usr/bin/pypy /home/philippos/Documents/scripts/l14fix.py >/dev/null
WantedBy=multi-user.target

[Install]
WantedBy=multi-user.target
'''
# - If you dont have pypy, you can use python2 instead. Replace every "commands" with "subprocess" below for python3.
# - Enable systemd service with "systemctl enable l14fix.service"
# - Any BIOS or software updates may render this disfunctional


import os
import math
import commands

# Wait 20 seconds for sensors to be initialised
os.system("sleep 20")

# Some other useful commands for my laptop
os.system("echo 80 | sudo tee /sys/class/power_supply/BAT0/charge_stop_threshold")
os.system("sudo auditctl -e 0")

# Disable waking up on all other events except the lid and the power button
wakefix="cat /proc/acpi/wakeup | awk '{if(($3==\"*enabled\") && ($1!=\"LID\") && ($1!=\"SLPB\")) print $1}'| sudo tee /proc/acpi/wakeup"
# (Actually does it one on each iteration but fine for now)

# Keep a steady TDP to 20W (originally L14 balanced mode seems to be 30W -> 25W -> 12W)
tdpfix = "sudo ryzenadj --stapm-limit=20000 --fast-limit=20000 --slow-limit=20000 ; "

# Request to default to fan auto mode, if 60 seconds pass without intervention from this script
os.system("echo watchdog 60 | sudo tee /proc/acpi/ibm/fan")

minumum_fan_speed = 1 # an integer from 0 to 7

counter = 0

while True:
	
	# Read GPU and CPU temperatures and create a custom function for a value between 0-7
	tgpu = int(commands.getoutput("sensors|grep edge").split("+")[1].split(".")[0])
	tdie = int(commands.getoutput("sensors|grep Tdie").split("+")[1].split(".")[0])
	level1 = min(max(tgpu, 52),59)-52
	level2 = min(7,(min(max(tdie, 65),90)-65)/3)
	level=max(level1,level2,minumum_fan_speed)
	print (level1,level2,level)
	
	# Update fan level
	os.system("echo level %d | sudo tee /proc/acpi/ibm/fan"%(level,))
	
	# Also every 2 minutes update the other states in case they have been removed (e.g. from connecting the power supply)		
	if counter==0:
		os.system(tdpfix+wakefix)
	counter=(counter+1)%24
	
	# Repeat every 5 seconds
	os.system("sleep 5")
