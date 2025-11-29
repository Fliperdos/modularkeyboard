from kmk.scanners.digitalio import MatrixScanner
from adafruit_mcp230xx.mcp23017 import MCP23017
from kmk.scanners import DiodeOrientation
from kmk.keys import KC

class ModularNumpad:
    def __init__(self, i2c, addr):
        super().__init__()
        self.name='Numpad'
        self.i2c=i2c
        self.addr=addr
        self.mcp=None
        

    def connect(self):
        try: 
            self.mcp = MCP23017(self.i2c, self.addr)
            print(f'### {self.name} connected!')

        except Exception as e: 
            self.mcp=None
            print(f'### {self.name} Not Connected: {e}')

    def get_matrix(self):
        if self.mcp:
            return MatrixScanner(cols=(self.mcp.get_pin(8),),
                                rows=(self.mcp.get_pin(9), self.mcp.get_pin(7)),
                                diode_orientation=DiodeOrientation.COL2ROW)
        else: return None
    
    def get_keymap(self):
        if self.mcp: return [KC.P1, KC.P2]
        else: return None