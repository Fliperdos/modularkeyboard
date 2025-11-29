import board
import busio
from kb import Modularkeyboard
import supervisor

i2c=None
try: i2c=busio.I2C(board.GP17, board.GP16,) 
except Exception as e: print(f'I2C error: {e}')

keyboard = Modularkeyboard(i2c)
keyboard.debug_enabled = True

while True:
    try:
        keyboard.go()
    except OSError as e: 
        print(f'{e} Error')

#ab12ab1122aaab12211ab1abaababab12ab
#abab121122