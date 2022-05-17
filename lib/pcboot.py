import uasyncio
from lib.neopixel import Neopixel

#Colour Table
red = (255, 0, 0)
orange = (255, 50, 0)
yellow = (255, 100, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (100, 0, 90)
violet = (200, 0, 100)
off = (0, 0, 0)

class pc_boot:
    
        def __init__(self, strip, length, speed, callback) -> None:
            self.current_task = None
            self.length = length
            self.strip = strip
            self.speed = speed
            self.callback = callback
        
        async def boot_up(self):
            for j in range(3):
                    #print(j)
                    #print(pcBooted)
                    #pcPixels.brightness(10*(j*2)) #adjust brightness each cycle
                    for i in range(0, 8, 1):
                        self.strip.set_pixel(i + 8, blue)
                        self.strip.set_pixel(7 - i, blue)
                        self.strip.show()
                        await uasyncio.sleep_ms(self.speed)
                    for i in range(0, 8, 1):
                        self.strip.set_pixel(i + 8, off)
                        self.strip.set_pixel(7 - i, off)
                        self.strip.show()
                        await uasyncio.sleep_ms(self.speed)
                    if j == 2:
                        await uasyncio.sleep_ms(self.speed)
                        self.strip.fill(off)

        async def loop(self):
            await self.boot_up()
            await uasyncio.sleep_ms(self.speed)
            self.callback()

        def start(self):
            self.current_task = uasyncio.create_task(self.loop())

        def stop(self):
            self.current_task.cancel()           
