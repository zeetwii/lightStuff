from gpiozero import LED # needed to control the LED (laser)
import time # needed for sleep function

import board # needed for neopixels
import neopixel # needed for neopixels


class LightStuff:
    def __init__(self, laser_pin=23, neopixel_pin=18, num_pixels=7):
        self.led = LED(laser_pin) # create an LED object on the specified pin
        self.turn_off() # ensure the LED is off initially

        self.pixels = neopixel.NeoPixel(board.D18, num_pixels, brightness=1, auto_write=True, pixel_order=neopixel.RGBW)
        self.pixels.fill((0, 0, 0, 0))  # Turn off all pixels initially
        self.pixels.show()

        self.morse_code_dict = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

    def turn_on(self):
        self.led.on() # turn the LED on

    def turn_off(self):
        self.led.off() # turn the LED off

    def blink(self, on_time=1, off_time=1, n=None):
        """
        Blink the LED a specified number of times with given on and off durations.

        Args:
            on_time (int, optional): How long to stay on in seconds. Defaults to 1.
            off_time (int, optional): How long to stay off in seconds. Defaults to 1.
            n (_type_, optional): How many times to repeat. Defaults to None.
        """
        self.turn_on() # turn the LED on
        time.sleep(on_time) # wait for the specified on time
        self.turn_off() # turn the LED off
        time.sleep(off_time) # wait for the specified off time

        if n is not None:
            for _ in range(n - 1): # blink n times in total
                self.turn_on()
                time.sleep(on_time)
                self.turn_off()
                time.sleep(off_time)
                
    def send_morse_code(self, message, dot_duration=0.2):
        """
        Send a message in Morse code using the LED.

        Args:
            message (str): The message to send in Morse code.
            dot_duration (float, optional): Duration of a dot in seconds. Defaults to 0.2.
        """
        dash_duration = dot_duration * 3
        intra_char_space = dot_duration
        inter_char_space = dot_duration * 3
        inter_word_space = dot_duration * 7

        for char in message.upper():
            if char == ' ':
                time.sleep(inter_word_space) # space between words
                continue

            morse_code = self.morse_code_dict.get(char, '')
            for symbol in morse_code:
                if symbol == '.':
                    self.turn_on()
                    self.pixels.fill((0, 0, 255, 0))  # Blue for dot
                    time.sleep(dot_duration)
                    self.turn_off()
                    self.pixels.fill((0, 0, 0, 0))  # Turn off pixels
                elif symbol == '-':
                    self.turn_on()
                    self.pixels.fill((255, 0, 0, 0))  # Red for dash
                    time.sleep(dash_duration)
                    self.turn_off()
                    self.pixels.fill((0, 0, 0, 0))  # Turn off pixels
                time.sleep(intra_char_space) # space between symbols

            time.sleep(inter_char_space - intra_char_space) # space between characters
    
if __name__ == "__main__":
    light = LightStuff(pin=26) # create a LightStuff object on GPIO pin 26
    light.blink(on_time=0.5, off_time=0.5, n=3) # blink the LED 3 times

    while True:
        message = input("Enter a message to send in Morse code: ")
        light.send_morse_code(message, dot_duration=0.2) # send message in Morse code