from neopixel import Neopixel
import machine
from machine import Pin, I2C
import uasyncio
from abutton import Pushbutton
import time
from ssd1306 import SSD1306_I2C
from oledidle import oled_idling
from oledfire import oled_firing
from pcidle import pc_idle
from pcboot import pc_boot
from oledboot import oled_boot

# #Various Variables
pcSpeed = 50
oledSpeed = 50
oledBootSpeed = 250
pcBooted = False

#Setup OLED on i2C
i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 32, i2c)

#Setup Fire Button
mybutton = Pushbutton(Pin(15, Pin.IN, Pin.PULL_DOWN))

#Pico LED for blinkingtest
led = Pin(25, Pin.OUT)

#Setup Neopixels
num_pcPixels = 16
pcPixels = Neopixel(num_pcPixels, 0, 2, "GRB")
pcPixels.fill((0, 0, 0))
pcPixels.brightness(1)
        
# #oled boot sequence
# async def oledboot(speed, booted_callback):
#         oled.fill(0)
#         oled.text("Loading", 0, 0)
#         oled.text("SPENGLER.ROM", 0, 8)
#         oled.show()
#         await uasyncio.sleep_ms(speed)
#         oled.fill(0)
#         oled.text("Loading", 0, 0)
#         oled.text("SPENGLER.ROM.", 0, 8)
#         oled.show()
#         await uasyncio.sleep_ms(speed)
#         oled.fill(0)
#         oled.text("Loading", 0, 0)
#         oled.text("SPENGLER.ROM..", 0, 8)
#         oled.show()
#         await uasyncio.sleep_ms(speed)
#         oled.fill(0)
#         oled.text("Loading", 0, 0)
#         oled.text("SPENGLER.ROM...", 0, 8)
#         oled.show()
#         await uasyncio.sleep_ms(speed)
#         oled.fill(0)
#         oled.text("Loading", 0, 0)
#         oled.text("SPENGLER.ROM....", 0, 8)
#         oled.show()
#         await uasyncio.sleep_ms(speed)
#         oled.fill(0)
#         oled.fill_rect(0,0,128,8,1)
#         oled.text("COMPLETE", 0, 0, 0)
#         oled.text("SPENGLER.ROM....", 0, 8)
#         oled.text("Syncing Gen...", 0, 16)
#         oled.show()
#         await uasyncio.sleep_ms(speed)
#         oled.fill(0)
#         oled.fill_rect(0,0,128,8,1)
#         oled.text("COMPLETE", 0, 0, 0)
#         oled.text("SPENGLER.ROM....", 0, 8)
#         oled.text("Syncing Gen...", 0, 16)
#         oled.text("Boot Cyclo...", 0, 24)
#         oled.show()
#         oled.fill(0)
#         booted_callback()

blinkingtask = None

async def toggleled():
    while True:
        led.toggle()
        await uasyncio.sleep_ms(50)
    
def start_toggle():
    global blinkingtask
    blinkingtask = uasyncio.create_task(toggleled())
    idle_status.stop()
    fire_status.start()


def stop_toggle():
    global blinkingtask
    blinkingtask.cancel()
    led.value(0)
    idle_status.start()
    fire_status.stop()
    
def pc_go_idle():
    pc_idling.start()

def oled_go_idle():
    idle_status.start()
    
async def main():
    while True:
        await uasyncio.sleep_ms(1000)
        
idle_status = oled_idling(oled, oledSpeed)
fire_status = oled_firing(oled, oledSpeed)
pc_idling = pc_idle(pcPixels, num_pcPixels, pcSpeed)
pc_boot =  pc_boot(pcPixels, num_pcPixels, pcSpeed, pc_go_idle)
oled_boot = oled_boot(oled, oledBootSpeed, oled_go_idle)

pc_boot.start()
oled_boot.start()

mybutton.press_func(start_toggle)
mybutton.release_func(stop_toggle) 

while True:
    uasyncio.run(main())
    