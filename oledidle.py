import uasyncio

class oled_idling:
    
        def __init__(self, oled, speed) -> None:
            self.current_task = None
            self.oled = oled
            self.speed = speed
            
        async def move_up(self):
            for i in range(0, 128, 8):
                self.oled.fill_rect(i,0,7,32,1)
                self.oled.show()
                await uasyncio.sleep_ms(self.speed)
                self.oled.fill(0)


        async def move_down(self):
            for i in range(120, 0, -8):
                self.oled.fill_rect(i,0,7,32,1)
                self.oled.show()
                await uasyncio.sleep_ms(self.speed)
                self.oled.fill(0)


        async def loop(self):
            while True:
                await self.move_up()
                await self.move_down()



        def start(self):
            self.current_task = uasyncio.create_task(self.loop())

        def stop(self):
            self.current_task.cancel()
            self.oled.fill(0)
            self.oled.show()
