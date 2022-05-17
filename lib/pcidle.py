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

class pc_idle:
    
        def __init__(self, strip, length, speed) -> None:
            self.current_task = None
            self.length = length
            self.strip = strip
            self.speed = speed                
        
        async def move_up(self):
            #
            for i in range(self.length):
                self.strip.set_pixel(i, blue)
                self.strip.show()
                await uasyncio.sleep_ms(self.speed)
           
        async def move_down(self):
            #
            for i in range(self.length - 1, -1, -1):
                self.strip.set_pixel(i, off)
                self.strip.show()
                await uasyncio.sleep_ms(self.speed)
                if i == 0:
                    self.strip.fill(off)            

        async def loop(self):
            while True:
                await self.move_up()
                await self.move_down()

        def start(self):
            self.current_task = uasyncio.create_task(self.loop())

        def stop(self):
            self.current_task.cancel()           