import RPi.GPIO as GPIO
import time
import os

from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep, strftime
from datetime import datetime

ausgang = 37    # 

def setup():
    
    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
    GPIO.setup(ausgang, GPIO.OUT)   # set the ledPin to OUTPUT mode
    GPIO.output(ausgang, GPIO.LOW)  # make ledPin output LOW level 
    print ('using pin%d'%ausgang)


def schleife():
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    while True:
        print ('Temperatur-Check')
        #print (tempCheck())
        tempakt01 = getCpuTemperature()
        print (tempakt01)
        bewertung = tempCheck()
        
        if bewertung == 2:
            print ('Lüfter ein <<<')
            GPIO.output(ausgang, GPIO.LOW)
            lcd.clear()
            lcd.setCursor(0,0)  # set cursor position
            lcd.message( 'Bayern 2' )#
            lcd.message( 'Freiburg 1')   
        else:
            print ('Lüfter aus <<<')
            GPIO.output(ausgang, GPIO.HIGH)
            lcd.clear()
            lcd.setCursor(0,0)  # set cursor position
            lcd.message(getCpuTemperature_01())
            #lcd.message( 'Leipzig 2')  
            
        time.sleep(10)                   # Wait for 10 second
        #os.system("vcgencmd measure_temp")
        #print (getCpuTemperature())


def getCpuTemperature():  
  tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )  
  cpu_temp = tempFile.read()  
  tempFile.close()
  tempakt = float(cpu_temp)/1000
  return tempakt

def getCpuTemperature_01():  
  tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )  
  cpu_temp = tempFile.read()  
  tempFile.close()
  #tempakt = float(cpu_temp)/1000
  #return cpu_temp
  return '{:.2f}'.format( float(cpu_temp)/1000 ) + ' C'


def tempCheck():
    tempakt02 = getCpuTemperature()
    if tempakt02 < 60:
        return  1
    else:
        return  2

PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)



if __name__ == '__main__':    # Program entrance
    print ('Program is starting ... \n')
    setup()
    try:
        schleife()
        
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        GPIO.output(ausgang, GPIO.LOW)
        print ("Lüfter aus <<<")
        lcd.clear()
        GPIO.cleanup()

