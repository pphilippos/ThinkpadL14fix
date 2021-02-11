# ThinkPad L14 fix

A quick and dirty python script to fix some issues with ThinkPad L14 AMD. 

This is the script I use on my own ThinkPad L14 to fix the [problem](https://forums.lenovo.com/topic/findpost/1304/5044792/5164364) with the fan only accelerating and also the unexpected waking up from sleep. It comes with ABSOLUTELY NO WARRANTY for use on your personal machine.

It relies on existing tools like the thinkpad_acpi. Please study the script comments for more information. On your personal machine you may require a different fan speed curve etc...

Tested on Arch Linux. Problematic BIOS version: 1.10, 1.12.

It can be run as root, i.e. ```sudo python2 l14fix.py```, or as a service (see comments).

#### Update (Thu Feb 11 2021):

The 2nd version (``l14fix2.py``) also adjusts TDP based on temperature (as at 2-4 threads it can reach over 95 C, but at 16 threads there is no throttling at 25 W (running at ~75C)). It also drops to 5W when on battery (slow), but you can adjust it to your preferences. The fan problem still persists with BIOS version 1.13.
