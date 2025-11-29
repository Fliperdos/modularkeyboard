from kmk.scanners.digitalio import MatrixScanner
from adafruit_mcp230xx.mcp23017 import MCP23017
from kmk.scanners import DiodeOrientation
from kmk.modules import Module
import board
from kmk.keys import KC
import rotaryio

class ModularEncoder:
    def __init__(self, i2c, addr):
        self.name = 'Encoder'
        self.i2c = i2c
        self.addr = addr
        self.mcp=None
        self.encoder=None
        self.last_pos=None

    def connect(self):
        try: 
            self.mcp = MCP23017(self.i2c, self.addr)
            self.encoder = rotaryio.IncrementalEncoder(
                board.GP0, board.GP1,)
            print(f'### {self.name} connected!')

        except Exception as e: 
            self.mcp=None
            print(f'### {self.name} Not Connected: {e}')

    def get_matrix(self):
        if self.mcp:
            return MatrixScanner(cols=(self.mcp.get_pin(8),),
                                 rows=(self.mcp.get_pin(9),),
                                 diode_orientation=DiodeOrientation.COL2ROW)
        else: return None
        
    def get_keymap(self):
        if self.mcp: return [KC.P1]
        else: return None


    def encoder_scan(self):
        if self.mcp:
            pos = self.encoder.position
            print(f'Encoder position: {pos}'  #chyba -->  )

            self.last_pos = pos
            
        else: pass
