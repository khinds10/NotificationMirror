import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
from Adafruit_LED_Backpack import Matrix8x8
from bitarray import bitarray
import binascii
import collections

# all the displays
displays = [Matrix8x8.Matrix8x8(address=0x70), Matrix8x8.Matrix8x8(address=0x71), Matrix8x8.Matrix8x8(address=0x72), Matrix8x8.Matrix8x8(address=0x73), Matrix8x8.Matrix8x8(address=0x74), Matrix8x8.Matrix8x8(address=0x75)] #, Matrix8x8.Matrix8x8(address=0x76)

# custom font for matrix display
matrixCustomFont = {}
matrixCustomFont[' '] = '\x00\x00\x00\x00\x00\x00\x00\x00'
matrixCustomFont['!'] = '\x30\x78\x78\x30\x30\x00\x30\x00'
matrixCustomFont['$'] = '\x18\x3E\x60\x3C\x06\x7C\x18\x00'
matrixCustomFont['%'] = '\x00\x63\x66\x0C\x18\x33\x63\x00'
matrixCustomFont['&'] = '\x1C\x36\x1C\x3B\x6E\x66\x3B\x00'
matrixCustomFont["'"] = '\x30\x30\x60\x00\x00\x00\x00\x00'
matrixCustomFont['('] = '\x0C\x18\x30\x30\x30\x18\x0C\x00'
matrixCustomFont[')'] = '\x30\x18\x0C\x0C\x0C\x18\x30\x00'
matrixCustomFont['*'] = '\x00\x66\x3C\xFF\x3C\x66\x00\x00'
matrixCustomFont['+'] = '\x00\x30\x30\xFC\x30\x30\x00\x00'
matrixCustomFont[','] = '\x00\x00\x00\x00\x00\x18\x18\x30'
matrixCustomFont['-'] = '\x00\x00\x00\x7E\x00\x00\x00\x00'
matrixCustomFont['.'] = '\x00\x00\x00\x00\x00\x18\x18\x00'
matrixCustomFont['/'] = '\x03\x06\x0C\x18\x30\x60\x40\x00'
matrixCustomFont['1'] = '\x18\x38\x58\x18\x18\x18\x7E\x00'
matrixCustomFont['2'] = '\x3C\x66\x06\x1C\x30\x66\x7E\x00'
matrixCustomFont['3'] = '\x3C\x66\x06\x1C\x06\x66\x3C\x00'
matrixCustomFont['4'] = '\x0E\x1E\x36\x66\x7F\x06\x0F\x00'
matrixCustomFont['5'] = '\x7E\x60\x7C\x06\x06\x66\x3C\x00'
matrixCustomFont['6'] = '\x1C\x30\x60\x7C\x66\x66\x3C\x00'
matrixCustomFont['7'] = '\x7E\x66\x06\x0C\x18\x18\x18\x00'
matrixCustomFont['8'] = '\x3C\x66\x66\x3C\x66\x66\x3C\x00'
matrixCustomFont['9'] = '\x3C\x66\x66\x3E\x06\x0C\x38\x00'
matrixCustomFont[':'] = '\x00\x18\x18\x00\x00\x18\x18\x00'
matrixCustomFont[';'] = '\x00\x18\x18\x00\x00\x18\x18\x30'
matrixCustomFont['<'] = '\x0C\x18\x30\x60\x30\x18\x0C\x00'
matrixCustomFont['='] = '\x00\x00\x7E\x00\x00\x7E\x00\x00'
matrixCustomFont['>'] = '\x30\x18\x0C\x06\x0C\x18\x30\x00'
matrixCustomFont['?'] = '\x3C\x66\x06\x0C\x18\x00\x18\x00'
matrixCustomFont['@'] = '\x3E\x63\x6F\x69\x6F\x60\x3E\x00'
matrixCustomFont['A'] = '\x18\x3C\x66\x66\x7E\x66\x66\x00'
matrixCustomFont['B'] = '\x7E\x33\x33\x3E\x33\x33\x7E\x00'
matrixCustomFont['C'] = '\x1E\x33\x60\x60\x60\x33\x1E\x00'
matrixCustomFont['D'] = '\x7C\x36\x33\x33\x33\x36\x7C\x00'
matrixCustomFont['E'] = '\x7F\x31\x34\x3C\x34\x31\x7F\x00'
matrixCustomFont['F'] = '\x7F\x31\x34\x3C\x34\x30\x78\x00'
matrixCustomFont['G'] = '\x1E\x33\x60\x60\x67\x33\x1F\x00'
matrixCustomFont['H'] = '\x66\x66\x66\x7E\x66\x66\x66\x00'
matrixCustomFont['I'] = '\x3C\x18\x18\x18\x18\x18\x3C\x00'
matrixCustomFont['J'] = '\x0F\x06\x06\x06\x66\x66\x3C\x00'
matrixCustomFont['K'] = '\x73\x33\x36\x3C\x36\x33\x73\x00'
matrixCustomFont['L'] = '\x78\x30\x30\x30\x31\x33\x7F\x00'
matrixCustomFont['M'] = '\x63\x77\x7F\x7F\x6B\x63\x63\x00'
matrixCustomFont['N'] = '\x63\x73\x7B\x6F\x67\x63\x63\x00'
matrixCustomFont['O'] = '\x3E\x63\x63\x63\x63\x63\x3E\x00'
matrixCustomFont['P'] = '\x7E\x33\x33\x3E\x30\x30\x78\x00'
matrixCustomFont['Q'] = '\x3C\x66\x66\x66\x6E\x3C\x0E\x00'
matrixCustomFont['R'] = '\x7E\x33\x33\x3E\x36\x33\x73\x00'
matrixCustomFont['S'] = '\x3C\x66\x30\x18\x0C\x66\x3C\x00'
matrixCustomFont['T'] = '\x7E\x5A\x18\x18\x18\x18\x3C\x00'
matrixCustomFont['U'] = '\x66\x66\x66\x66\x66\x66\x7E\x00'
matrixCustomFont['V'] = '\x66\x66\x66\x66\x66\x3C\x18\x00'
matrixCustomFont['W'] = '\x63\x63\x63\x6B\x7F\x77\x63\x00'
matrixCustomFont['X'] = '\x63\x63\x36\x1C\x1C\x36\x63\x00'
matrixCustomFont['Y'] = '\x66\x66\x66\x3C\x18\x18\x3C\x00'
matrixCustomFont['Z'] = '\x7F\x63\x46\x0C\x19\x33\x7F\x00'
matrixCustomFont['['] = '\x3C\x30\x30\x30\x30\x30\x3C\x00'
matrixCustomFont[']'] = '\x3C\x0C\x0C\x0C\x0C\x0C\x3C\x00'
matrixCustomFont['^'] = '\x08\x1C\x36\x63\x00\x00\x00\x00'
matrixCustomFont['_'] = '\x00\x00\x00\x00\x00\x00\x00\xFF'
matrixCustomFont['`'] = '\x18\x18\x0C\x00\x00\x00\x00\x00'
matrixCustomFont['a'] = '\x00\x00\x3C\x06\x3E\x66\x3B\x00'
matrixCustomFont['b'] = '\x70\x30\x3E\x33\x33\x33\x6E\x00'
matrixCustomFont['c'] = '\x00\x00\x3C\x66\x60\x66\x3C\x00'
matrixCustomFont['d'] = '\x0E\x06\x3E\x66\x66\x66\x3B\x00'
matrixCustomFont['e'] = '\x00\x00\x3C\x66\x7E\x60\x3C\x00'
matrixCustomFont['f'] = '\x1C\x36\x30\x78\x30\x30\x78\x00'
matrixCustomFont['g'] = '\x00\x00\x3B\x66\x66\x3E\x06\x7C'
matrixCustomFont['h'] = '\x70\x30\x36\x3B\x33\x33\x73\x00'
matrixCustomFont['i'] = '\x18\x00\x38\x18\x18\x18\x3C\x00'
matrixCustomFont['j'] = '\x06\x00\x06\x06\x06\x66\x66\x3C'
matrixCustomFont['k'] = '\x70\x30\x33\x36\x3C\x36\x73\x00'
matrixCustomFont['l'] = '\x38\x18\x18\x18\x18\x18\x3C\x00'
matrixCustomFont['m'] = '\x00\x00\x66\x7F\x7F\x6B\x63\x00'
matrixCustomFont['n'] = '\x00\x00\x7C\x66\x66\x66\x66\x00'
matrixCustomFont['o'] = '\x00\x00\x3C\x66\x66\x66\x3C\x00'
matrixCustomFont['p'] = '\x00\x00\x6E\x33\x33\x3E\x30\x78'
matrixCustomFont['q'] = '\x00\x00\x3B\x66\x66\x3E\x06\x0F'
matrixCustomFont['r'] = '\x00\x00\x6E\x3B\x33\x30\x78\x00'
matrixCustomFont['s'] = '\x00\x00\x3E\x60\x3C\x06\x7C\x00'
matrixCustomFont['t'] = '\x08\x18\x3E\x18\x18\x1A\x0C\x00'
matrixCustomFont['u'] = '\x00\x00\x66\x66\x66\x66\x3B\x00'
matrixCustomFont['v'] = '\x00\x00\x66\x66\x66\x3C\x18\x00'
matrixCustomFont['w'] = '\x00\x00\x63\x6B\x7F\x7F\x36\x00'
matrixCustomFont['x'] = '\x00\x00\x63\x36\x1C\x36\x63\x00'
matrixCustomFont['y'] = '\x00\x00\x66\x66\x66\x3E\x06\x7C'
matrixCustomFont['z'] = '\x00\x00\x7E\x4C\x18\x32\x7E\x00'
matrixCustomFont["'"] = '\x0E\x18\x18\x70\x18\x18\x0E\x00'
matrixCustomFont['|'] = '\x0C\x0C\x0C\x00\x0C\x0C\x0C\x00'
matrixCustomFont['}'] = '\x70\x18\x18\x0E\x18\x18\x70\x00'
matrixCustomFont['~'] = '\x3B\x6E\x00\x00\x00\x00\x00\x00'

def resetDisplays():
    """ setup all the displays and reset to blank """
    for display in range(0, 6):
        displays[display].begin()
        displays[display].clear()
        displays[display].write_display()

def rotate(matrix, degree):
    """ rotate 2d array by degree """
    if degree == 0:
        return matrix
    elif degree > 0:
        return rotate(zip(*matrix[::-1]), degree-90)
    else:
        return rotate(zip(*matrix)[::-1], degree+90)
    
def chunks(l, n):
    """ break list into 2d array chunks """
    return [l[i:i+n] for i in range(0, len(l), n)]

def displayCharByDisplay(char, display):
    """ show single character on given display """

    bitArray = bitarray()
    bitArray.frombytes(matrixCustomFont[char])
    rotatedBits = rotate(chunks(bitArray.tolist(),8),90)
    pixels = []
    count = 0
    for x in range(0, 8):
        for y in range(0, 8):
            pixels.append(rotatedBits[x][y])
            count = count + 1
    image = Image.new('1', (8, 8))
    image.putdata(pixels)
    draw = ImageDraw.Draw(image)
    display.set_image(image)
    display.write_display()


def showText(text):
    """ show text on displays """
    
    # group text into 7 blocks long and display on displays sequentially
    textGrouped = [text[i:i+8] for i in range(0, len(text), 8)]
    
    for x in range(0, 10):
        for textEntry in textGrouped:
            for x in range(0, 6):
                displayCharByDisplay(textEntry[x], displays[x])
                try:
                    displayCharByDisplay(textEntry[x], displays[x])
                except:
                    displayCharByDisplay(" ", displays[x])
            time.sleep(0.15)
        resetDisplays()
        time.sleep(5)
        
resetDisplays()

# this text has to be multiple of 7 else it will crash on the last word :(
try:
    showText('adds a single element to the end of the list. list.insert(index, elem) -- inserts the element at the given index, shifting elements to the right. list.extend(list2) adds the elements in list2 to the end of the list.')
except:
    pass








