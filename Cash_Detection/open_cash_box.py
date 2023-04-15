import RPi.GPIO as GPIO
import time

def main():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(40,GPIO.OUT)
        GPIO.output(40,True)
        time.sleep(.1)
        GPIO.output(40,False)
        GPIO.cleanup()


if __name__ == "__main__":
        main()