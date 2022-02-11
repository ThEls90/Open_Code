import RPi.GPIO as GPIO
import time
import os

ausgang = 37    # 

def setup():
    
    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
    GPIO.setup(ausgang, GPIO.OUT)   # set the ledPin to OUTPUT mode
    GPIO.output(ausgang, GPIO.LOW)  # make ledPin output LOW level 
    print ('using pin%d'%ausgang)

def schleife():
    while True:
        print ('Temperatur-Check')
        #print (tempCheck())
        tempakt01 = getCpuTemperature()
        print (tempakt01)
        bewertung = tempCheck()
        
        if bewertung == 2:
            print ('Lüfter ein <<<')
            GPIO.output(ausgang, GPIO.LOW)
        else:
            print ('Lüfter aus <<<')
            GPIO.output(ausgang, GPIO.HIGH)
            
        time.sleep(10)                   # Wait for 10 second
        #os.system("vcgencmd measure_temp")
        #print (getCpuTemperature())


def getCpuTemperature():  
  tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )  
  cpu_temp = tempFile.read()  
  tempFile.close()
  tempakt = float(cpu_temp)/1000
  return tempakt

def tempCheck():
    tempakt02 = getCpuTemperature()
    if tempakt02 < 60:
        return  1
    else:
        return  2
    


if __name__ == '__main__':    # Program entrance
    print ('Program is starting ... \n')
    setup()
    try:
        schleife()
        
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        GPIO.output(ausgang, GPIO.LOW)
        print ("Lüfter aus <<<")
        GPIO.cleanup()

