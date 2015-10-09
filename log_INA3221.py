#!/usr/bin/env python
#
# INA3221 Power Logger
# by Danny Iland
# 
# Based on testSDL_Pi_INA3221
# originally written by John C. Shovic,
# SwitchDoc Labs, 03/05/2015
#

# imports

import sys
import time
import datetime
import random 
import SDL_Pi_INA3221

# Two options to be used as timesamps in the log file.
# the first is human readable time
# The second is epoch style millisecond time
# Uncomment the one you want.

current_time = lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#current_time = lambda: int(round(time.time() * 1000))


filename = time.strftime("%Y-%m-%d%H%M") + "_power_measurements.txt"
output_file = open(filename, 'w')

print "Power Logging Started at: "+ time.strftime("%Y-%m-%d %H:%M:%S")

output_file.write("time, current (mA), voltage")

ina3221 = SDL_Pi_INA3221.SDL_Pi_INA3221(addr=0x40)

# Configuration

# The breakout board is only good up to ~3A current with existing shunts.

# Put the 1st channel between battery and charge controller
BATTERY_CHANNEL = 1
# Put 2nd channel between panel and charge controller. 
SOLAR_CHANNEL   = 2
# Put 3rd channel between charge controller and load
OUTPUT_CHANNEL  = 3


while True:

  	print "------------------------------"
  	shuntvoltage1 = 0
  	busvoltage1   = 0
  	current_mA1   = 0
  	loadvoltage1  = 0


  	busvoltage1 = ina3221.getBusVoltage_V(BATTERY_CHANNEL)
  	shuntvoltage1 = ina3221.getShuntVoltage_mV(BATTERY_CHANNEL)
  	# minus is to get the "sense" right.   - means the battery is charging, + that it is discharging
  	current_mA1 = ina3221.getCurrent_mA(BATTERY_CHANNEL)  

  	loadvoltage1 = busvoltage1 + (shuntvoltage1 / 1000)
  
  	print "Battery Bus Voltage: %3.2f V " % busvoltage1
  	print "Battery Shunt Voltage: %3.2f mV " % shuntvoltage1
  	print "Battery Load Voltage:  %3.2f V" % loadvoltage1
  	print "Battery Current 1:  %3.2f mA" % current_mA1
  	print

  	shuntvoltage2 = 0
  	busvoltage2 = 0
  	current_mA2 = 0
  	loadvoltage2 = 0

  	busvoltage2 = ina3221.getBusVoltage_V(SOLAR_CHANNEL)
  	shuntvoltage2 = ina3221.getShuntVoltage_mV(SOLAR_CHANNEL)
  	current_mA2 = -ina3221.getCurrent_mA(SOLAR_CHANNEL)
  	loadvoltage2 = busvoltage2 + (shuntvoltage2 / 1000)
  
  	print "Solar Cell Bus Voltage 2:  %3.2f V " % busvoltage2
  	print "Solar Cell Shunt Voltage 2: %3.2f mV " % shuntvoltage2
  	print "Solar Cell Load Voltage 2:  %3.2f V" % loadvoltage2
  	print "Solar Cell Current 2:  %3.2f mA" % current_mA2
  	print 

  	shuntvoltage3 = 0
  	busvoltage3 = 0
  	current_mA3 = 0
  	loadvoltage3 = 0

  	busvoltage3 = ina3221.getBusVoltage_V(OUTPUT_CHANNEL)
  	shuntvoltage3 = ina3221.getShuntVoltage_mV(OUTPUT_CHANNEL)
  	current_mA3 = ina3221.getCurrent_mA(OUTPUT_CHANNEL)
  	loadvoltage3 = busvoltage3 + (shuntvoltage3 / 1000)
  
  	print "Output Bus Voltage 3:  %3.2f V " % busvoltage3
  	print "Output Shunt Voltage 3: %3.2f mV " % shuntvoltage3
  	print "Output Load Voltage 3:  %3.2f V" % loadvoltage3
  	print "Output Current 3:  %3.2f mA" % current_mA3
        
        output_file.write("%s,%s,%s\n" % (current_time(), loadvoltage3, current_mA3))
        output_file.flush()
        time.sleep(1.0)
