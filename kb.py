from kmk.scanners.digitalio import MatrixScanner
from kmk.scanners import DiodeOrientation
from kmk.kmk_keyboard import KMKKeyboard
from modules.numpad import ModularNumpad
from modules.encoder import ModularEncoder
from kmk.modules.encoder import EncoderHandler
from kmk.keys import Key
from kmk.keys import KC
import supervisor
import board
import time

int = False

class Modularkeyboard(KMKKeyboard):
    def __init__(self, i2c):
        super().__init__()

        self.i2c=i2c
        self.last_time = time.monotonic()

        self.keypad_module = ModularNumpad(i2c, 0x21)
        self.encoder_module = ModularEncoder(i2c, 0x20)

        self.modulars = [self.keypad_module, self.encoder_module]
        self.temp_matrix=[]
        self.temp_keymap=[]
        self.temp_enc_pins=[]
        self.temp_enc_map=[]
        self.encoders=False

        self.main_matrix = MatrixScanner(
            cols=(board.GP15,),
            rows=(board.GP14, board.GP13,),
            diode_orientation=DiodeOrientation.COL2ROW)

        self.main_keymap = [KC.A, KC.B]

        self.boot()

    def boot(self):
        self.temp_matrix = [self.main_matrix]
        self.temp_keymap = self.main_keymap
        self.last_scan = self.scan()
        print(f'== Boot scan: {self.last_scan}')

        for m in self.modulars:
            m.connect()
            if hasattr(m, 'encoder'):
                self.encoders = True

            if m.addr in self.last_scan:
                matrix = m.get_matrix()
                if matrix: self.temp_matrix.append(matrix)

                keymap = m.get_keymap()
                if keymap: self.temp_keymap.extend(keymap)

        self.matrix = tuple(self.temp_matrix)
        self.keymap = [self.temp_keymap]
        print(f'== Boot Matrix: {self.matrix}')
        print(f'== Boot KeyMap: {self.keymap}')


    def before_matrix_scan(self):
        super().before_matrix_scan()
        i = time.monotonic()
        scan = self.scan()

        self.encoder_module.encoder_scan()

        for m in self.modulars:
            if m.addr in self.scan() and hasattr(m, 'encoder'):
                m.encoder_scan()

        if i - self.last_time > 1:
            self.check(scan)


    def check(self, scan):
        if scan != self.last_scan:
            print('$$ Change detected, setup sarting')
            supervisor.reload() 
                

    def scan(self):
        try:
            while not self.i2c.try_lock(): pass
            try: return self.i2c.scan()
            finally: self.i2c.unlock()
        except Exception as e: print(e)






