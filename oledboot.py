import uasyncio

class oled_boot:
    
        def __init__(self, oled, speed, callback) -> None:
            self.current_task = None
            self.oled = oled
            self.speed = speed
            self.callback = callback
            
        async def boot_up(self):
            self.oled.fill(0)
            self.oled.text("Loading", 0, 0)
            self.oled.text("SPENGLER.ROM", 0, 8)
            self.oled.show()
            await uasyncio.sleep_ms(self.speed)
            self.oled.fill(0)
            self.oled.text("Loading", 0, 0)
            self.oled.text("SPENGLER.ROM.", 0, 8)
            self.oled.show()
            await uasyncio.sleep_ms(self.speed)
            self.oled.fill(0)
            self.oled.text("Loading", 0, 0)
            self.oled.text("SPENGLER.ROM..", 0, 8)
            self.oled.show()
            await uasyncio.sleep_ms(self.speed)
            self.oled.fill(0)
            self.oled.text("Loading", 0, 0)
            self.oled.text("SPENGLER.ROM...", 0, 8)
            self.oled.show()
            await uasyncio.sleep_ms(self.speed)
            self.oled.fill(0)
            self.oled.text("Loading", 0, 0)
            self.oled.text("SPENGLER.ROM....", 0, 8)
            self.oled.show()
            await uasyncio.sleep_ms(self.speed)
            self.oled.fill(0)
            self.oled.fill_rect(0,0,128,8,1)
            self.oled.text("COMPLETE", 0, 0, 0)
            self.oled.text("SPENGLER.ROM....", 0, 8)
            self.oled.text("Syncing Gen...", 0, 16)
            self.oled.show()
            await uasyncio.sleep_ms(self.speed)
            self.oled.fill(0)
            self.oled.fill_rect(0,0,128,8,1)
            self.oled.text("COMPLETE", 0, 0, 0)
            self.oled.text("SPENGLER.ROM....", 0, 8)
            self.oled.text("Syncing Gen...", 0, 16)
            self.oled.text("Boot Cyclo...", 0, 24)
            self.oled.show()
            self.oled.fill(0)
            await uasyncio.sleep_ms(self.speed)

        async def loop(self):
            await self.boot_up()
            await uasyncio.sleep_ms(self.speed)
            self.callback()

        def start(self):
            self.oled.fill(0)
            self.current_task = uasyncio.create_task(self.loop())

        def stop(self):
            self.current_task.cancel()
            self.oled.fill(0)
            self.oled.show()
