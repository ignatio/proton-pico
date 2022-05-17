import uasyncio

class oled_firing:
    
        def __init__(self, oled, speed) -> None:
            self.current_task = None
            self.oled = oled
            self.speed = speed
            
        async def bargraph(self):
            for i in range(0, 128, 8):
                if i == 120:
                    self.oled.fill(0)
                    i = 0
                self.oled.fill_rect(i,0,7,32,1)
                self.oled.show()
                await uasyncio.sleep_ms(self.speed)

        async def loop(self):
            while True:
                await self.bargraph()

        def start(self):
            self.oled.fill(0)
            self.current_task = uasyncio.create_task(self.loop())

        def stop(self):
            self.current_task.cancel()
            self.oled.fill(0)
            self.oled.show()