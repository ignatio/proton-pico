from dfplayermini import Player
import uasyncio
from time import sleep

EQNORM = 0x00
EQPOP = 0x01
EQROCK = 0x02
EQJAZZ = 0x03
EQCLAS = 0x04
EQBASS = 0x05

sequence_wait = None    

async def sequence_out(length, second_track):
    print("im in")
    global sequence_wait
    await uasyncio.sleep_ms(50)
    while music.playing():            
        await uasyncio.sleep_ms(length)    
    music.play(second_track)
    
def sequence(first_track, second_track):
    global sequence_wait
    sequence_wait = uasyncio.create_task(sequence_out(50, second_track))
    music.play(first_track)
     
music = Player(1, 8, 9, 14)

sequence(4, 1)

async def main():
    while True:
        await uasyncio.sleep_ms(1000)
        
while True:
    uasyncio.run(main())

# music.sequence(4, 2)

# music.volume(15)
# music.play(00, 000)
# sleep(10)
