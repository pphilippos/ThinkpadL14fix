# ThinkPad L14 fix

A quick and dirty python script to fix some issues with ThinkPad L14 AMD. 

This is the script I use on my own ThinkPad L14 to fix the [problem](https://forums.lenovo.com/topic/findpost/1304/5044792/5164364) with the fan only accelerating and also the unexpected waking up from sleep. It comes with ABSOLUTELY NO WARRANTY for use on your personal machine.

It relies on existing tools like the thinkpad_acpi. Please study the script comments for more information. On your personal machine you may require a different fan speed curve etc...

Tested on Arch Linux. Problematic BIOS version: 1.10, 1.12.

It can be run as root, i.e. ```sudo python2 l14fix.py```, or as a service (see comments).
