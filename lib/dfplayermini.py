import utime
from machine import UART, Timer, Pin
from utime import sleep_ms, ticks_ms, ticks_diff
import uasyncio

Start_Byte = 0x7E
Version_Byte = 0xFF
Command_Length = 0x06
Acknowledge = 0x00
End_Byte = 0xEF

EQNORM = 0x00
EQPOP = 0x01
EQROCK = 0x02
EQJAZZ = 0x03
EQCLAS = 0x04
EQBASS = 0x05

IDLE = 0
PAUSED = 1
PLAYING = 2

def split(num):
    return num >> 8, num & 0xFF

class Player:
    def __init__(self, uart, pin_TX, pin_RX, busy_pin):
    #def __init__(self):
        self.tx = pin_TX
        self.rx = pin_RX
        if busy_pin is not None:
            self.busy_pin = Pin(busy_pin, mode=Pin.IN, pull=Pin.PULL_UP)
        self.uart = UART(uart, 9600, parity=None, stop=1, bits=8, rx=Pin(self.rx), tx=Pin(self.tx)) # UART on 
        self.cmd(0x3F, 0x00)  # send initialization parametres
        self._fadeout_timer = Timer(-1)

        self._volume = 30
        self._max_volume = 30
        self._fadeout_speed = 0
    
    def cmd(self, CMD, Par2=0x00, Par1=0x00):
        Checksum = -(Version_Byte + Command_Length + CMD + Acknowledge + Par1 + Par2)
        HighByte, LowByte = split(Checksum)
        CommandLine = bytes([b & 0xFF for b in [
            Start_Byte, Version_Byte, Command_Length, CMD, Acknowledge,
            Par1, Par2, HighByte, LowByte, End_Byte
        ]])
        self.uart.write(CommandLine)
   
    
    def _fade_out_process(self, timer):
        new_volume = self._volume - self._fadeout_speed
        
        if new_volume <= 0:
            print("fadeout finished")
            new_volume = 0
            self._fadeout_timer.deinit()
            self.stop()
            new_volume = self._max_volume # reset volume to max 
        self.volume(new_volume)

    # playback

    def play(self, track_id=False):
        print(track_id)
        if not track_id:
            self.resume()
        elif track_id == 'next':
            self.cmd(0x01)
        elif track_id == 'prev':
            self.cmd(0x02)
        elif isinstance(track_id, int):
            self.cmd(0x03, track_id)

    def pause(self):
        self.cmd(0x0E)

    def resume(self):
        self.cmd(0x0D)

    def stop(self):
        self.cmd(0x16)

    def fadeout(self, fadeout_ms=1000):
        # more than 500ms and less than 3000ms
        fadeout_ms = int(sorted([500, fadeout_ms, 3000])[1])
        fade_out_step_ms = 100
        self._fadeout_speed = self._volume * \
            fade_out_step_ms / fadeout_ms  # ten steps per second
        self._fadeout_timer.init(
            period=fade_out_step_ms, callback=self._fade_out_process)

    def loop_track(self, track_id):
        self.cmd(0x08, track_id)

    def loop(self):
        self.cmd(0x19)

    def loop_disable(self):
        self.cmd(0x19, 0x01)
        
#     sequence_wait = None    
# 
#     async def sequence_out(self, length, second_track):
#         print("im in")
#         global sequence_wait
#         while self.playing():            
#             await uasyncio.sleep_ms(length)    
#         self.play(second_track)
#         #sequence_wait.cancel()
#         
#     def sequence(self, first_track, second_track):
#         global sequence_wait
#         sequence_wait = uasyncio.create_task(self.sequence_out(50, second_track))
#         self.play(first_track)
  

    def playing(self):
        if self.busy_pin is not None:
            #self.awaitplay()
            return self.busy_pin.value() == 0
        else:
            raise AssertionError("No busy pin provided, cannot detect play status")

   
    # volume control

    def volume_up(self):
        self._volume += 1
        self.cmd(0x04)

    def volume_down(self):
        self._volume -= 1
        self.cmd(0x05)

    def volume(self, volume=False):
        if volume:
            self._volume = int(sorted([0, volume, self._max_volume])[1])
            print("volume", self._volume)
            self.cmd(0x06, self._volume)
        
        return self._volume

    def eqset(self, eq_value):
        self.cmd(0x07, eq_value)
        
    # hardware

    def module_sleep(self):
        self.cmd(0x0A)

    def module_wake(self):
        self.cmd(0x0B)

    def module_reset(self):
        self.cmd(0x0C)
