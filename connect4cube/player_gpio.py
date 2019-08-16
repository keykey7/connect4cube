import logging
from time import sleep

from Adafruit_GPIO import GPIO

from connect4cube.player import BasePlayer

LOG = logging.getLogger(__name__)


class GpioPlayer(BasePlayer):
    """
    A binary-joystick controlled player using RasPi GPIOs
    https://pinout.xyz/
    """

    def __init__(self, north=5, east=6, south=12, west=13, button1=16):
        super().__init__()
        self.all_pins = [north, east, south, west, button1]
        self.clicked = False
        self.selected = (2, 2)
        self.gpio = GPIO.get_platform_gpio()
        for pin in self.all_pins:
            self.gpio.setup(pin, GPIO.IN, GPIO.PUD_DOWN)

    def __del__(self):
        for pin in self.all_pins:
            self.gpio.cleanup(pin)

    def gpio_callback(self, pin):
        """
        callback for joystick axis and buttons of the current player.
        see: https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
        :param pin: the GPIO pin nr
        :return: void
        """
        LOG.debug("GPIO callback @PIN {}".format(pin))
        if self.clicked:
            return  # too late to the party
        action = self.all_pins.index(pin)
        (x, y) = self.selected
        if action == 0 and y < 4:
            y += 1
        elif action == 1 and x < 4:
            x += 1
        elif action == 2 and y > 0:
            y -= 1
        elif action == 3 and x > 0:
            x -= 1
        elif action == 4:
            self.clicked = True
        self.selected = (x, y)
        LOG.debug("GPIO selected {},{}".format(x, y))
        self.do_select(x, y)

    def do_play(self) -> tuple:
        self.clicked = False
        for pin in self.all_pins:
            self.gpio.add_event_detect(pin, GPIO.RISING, self.gpio_callback, bouncetime=100)
        while not self.clicked:
            sleep(0.1)
        for pin in self.all_pins:
            self.gpio.remove_event_detect(pin)
        return self.selected
