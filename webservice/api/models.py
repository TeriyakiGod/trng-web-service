from enum import Enum

class RandomInt:
    def __init__(self, n: int = 10, min: int = 0, max: int = 10, repeat: bool = True):
        self.n = n
        self.min = min
        self.max = max
        self.repeat = repeat     
        
class RandomFloat:
    def __init__(self, n: int = 10, precision: int = 2):
        self.n = n
        self.precision = precision
        
class RandomString:
    def __init__(self, n: int = 10, m: int = 10, digits: bool = True, letters: bool = True, special: bool = False, repeat: bool = True):
        self.n = n
        self.m = m
        self.digits = digits
        self.letters = letters
        self.special = special
        self.repeat = repeat

class BytesFormat(Enum):
    HEX = "h"
    BINARY = "b"
    OCTAL = "o"
    DECIMAL = "d"

class RandomBytes:
    def __init__(self, n: int = 10, f: BytesFormat = BytesFormat.HEX):
        self.n = n
        self.f = f
        
class RandomSequence:
    def __init__(self, min: int = 0, max: int = 100):
        self.min = min
        self.max = max
        
class RandomCoin:
    def __init__(self, n: int = 10):
        self.n = n
        
class RandomDice:
    def __init__(self, n: int = 10, m: int = 6):
        self.n = n
        self.m = m

class RandomLotto:
    def __init__(self, n: int = 10):
        self.n = n
