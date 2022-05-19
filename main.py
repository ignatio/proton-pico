from lib.neopixel import Neopixel
import machine
from machine import Pin, I2C
import uasyncio
from lib.abutton import Pushbutton
from utime import sleep_ms
from lib.ssd1306 import SSD1306_I2C
from lib.oledidle import oled_idling
from lib.oledfire import oled_firing
from lib.pcidle import pc_idle
from lib.pcboot import pc_boot
from lib.oledboot import oled_boot
from lib.dfplayermini import Player

#DFPlayer (uart, rx, tx, busy)
music = Player(1, 8, 9, 14)

# #Various Variables
pcSpeed = 50
oledSpeed = 50
oledBootSpeed = 800
pcBooted = False

#Setup OLED on i2C
i2c=I2C(1,sda=Pin(6), scl=Pin(7), freq=400000)
oled = SSD1306_I2C(128, 32, i2c)

#Setup button objects
mybutton = Pushbutton(Pin(15, Pin.IN, Pin.PULL_UP))
busytrigger = Pushbutton(Pin(14, Pin.IN, Pin.PULL_UP))

#Pico LED for blinkingtest
led = Pin(25, Pin.OUT)

#Setup Neopixels
num_pcPixels = 16
pcPixels = Neopixel(num_pcPixels, 0, 2, "GRB")
pcPixels.fill((0, 0, 0))
pcPixels.brightness(1)
        
blinkingtask = None

sequence_wait = None

async def sequence_out_idle(length, second_track):
    print("im in")
    global sequence_wait
    await uasyncio.sleep_ms(length)
    while music.playing():            
        await uasyncio.sleep_ms(length)  
    music.play(second_track)
    music.loop()
    
def sequencetoidle(first_track, second_track):
    global sequence_wait
    music.loop_disable()
    music.stop()
    music.play(first_track)
    sequence_wait = uasyncio.create_task(sequence_out_idle(50, second_track))
    

async def toggleled():
    while True:
        led.toggle()
        await uasyncio.sleep_ms(50)
    
def start_toggle():
    global blinkingtask
    blinkingtask = uasyncio.create_task(toggleled())
    idle_status.stop()
    fire_status.start()
    music.loop_disable()
    music.stop()
    sequencetoidle(3, 3)


def stop_toggle():
    global blinkingtask
    blinkingtask.cancel()
    led.value(0)
    music.stop()
    sequencetoidle(4, 2)
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
sequencetoidle(1, 2)

mybutton.press_func(start_toggle)
mybutton.release_func(stop_toggle)

#busytrigger.release_func(music.play_next)

while True:
    uasyncio.run(main())
    