import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

row_pins = [board.GP2, board.GP3, board.GP4, board.GP5]
col_pins = [board.GP6, board.GP7, board.GP8, board.GP9, board.GP10]

rows = []
for pin in row_pins:
    r = digitalio.DigitalInOut(pin)
    r.direction = digitalio.Direction.OUTPUT
    r.value = True
    rows.append(r)

cols = []
for pin in col_pins:
    c = digitalio.DigitalInOut(pin)
    c.direction = digitalio.Direction.INPUT
    c.pull = digitalio.Pull.UP
    cols.append(c)

urls = [
    ["https://google.com", "https://youtube.com", "https://github.com", "https://discord.com", "https://reddit.com"],
    ["https://netflix.com", "https://spotify.com", "https://twitter.com", "https://instagram.com", "https://twitch.tv"],
    ["https://hackclub.com", "https://replit.com", "https://stackoverflow.com", "https://notion.so", "https://figma.com"],
    ["https://gmail.com", "https://google.com", "https://google.com", "https://google.com", "https://google.com"],
]

def open_url(url):
    keyboard.press(Keycode.GUI, Keycode.R)
    time.sleep(0.1)
    keyboard.release_all()
    time.sleep(0.4)
    layout.write(url)
    time.sleep(0.1)
    keyboard.press(Keycode.ENTER)
    time.sleep(0.05)
    keyboard.release_all()

pressed = [[False] * 5 for _ in range(4)]

while True:
    for r in range(4):
        rows[r].value = False
        time.sleep(0.001)
        for c in range(5):
            is_pressed = not cols[c].value
            if is_pressed and not pressed[r][c]:
                pressed[r][c] = True
                open_url(urls[r][c])
            elif not is_pressed:
                pressed[r][c] = False
        rows[r].value = True
    time.sleep(0.01)
