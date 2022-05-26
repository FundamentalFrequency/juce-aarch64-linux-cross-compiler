import atexit
import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    raise ImportError("This library requires the RPi.GPIO module\nInstall with: sudo pip install RPi.GPIO")


__version__ = '0.0.3'


DAT_PIN = 10
CLK_PIN = 11
LED_SOF = 0b11100000
LED_MAX_BR = 0b00011111

CHANNEL_PINS = [8, 7, 25, 24]

NUM_PIXELS_PER_CHANNEL = 16
NUM_CHANNELS = 4

DEFAULT_BRIGHTNESS = 0.2

_gamma_table = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
    2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5,
    6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 11, 11,
    11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18,
    19, 19, 20, 21, 21, 22, 22, 23, 23, 24, 25, 25, 26, 27, 27, 28,
    29, 29, 30, 31, 31, 32, 33, 34, 34, 35, 36, 37, 37, 38, 39, 40,
    40, 41, 42, 43, 44, 45, 46, 46, 47, 48, 49, 50, 51, 52, 53, 54,
    55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
    71, 72, 73, 74, 76, 77, 78, 79, 80, 81, 83, 84, 85, 86, 88, 89,
    90, 91, 93, 94, 95, 96, 98, 99, 100, 102, 103, 104, 106, 107, 109, 110,
    111, 113, 114, 116, 117, 119, 120, 121, 123, 124, 126, 128, 129, 131, 132, 134,
    135, 137, 138, 140, 142, 143, 145, 146, 148, 150, 151, 153, 155, 157, 158, 160,
    162, 163, 165, 167, 169, 170, 172, 174, 176, 178, 179, 181, 183, 185, 187, 189,
    191, 193, 194, 196, 198, 200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220,
    222, 224, 227, 229, 231, 233, 235, 237, 239, 241, 244, 246, 248, 250, 252, 255]

_white_point = (1.0, 1.0, 1.0)

_sleep_time = 0

pixels = [
    [[0, 0, 0, DEFAULT_BRIGHTNESS]] * NUM_PIXELS_PER_CHANNEL,
    [[0, 0, 0, DEFAULT_BRIGHTNESS]] * NUM_PIXELS_PER_CHANNEL,
    [[0, 0, 0, DEFAULT_BRIGHTNESS]] * NUM_PIXELS_PER_CHANNEL,
    [[0, 0, 0, DEFAULT_BRIGHTNESS]] * NUM_PIXELS_PER_CHANNEL
]

channels = [(16, False) for c in range(NUM_CHANNELS)]

_gpio_setup = False
_clear_on_exit = True


def _exit():
    if _clear_on_exit:
        clear()
        show()
    GPIO.cleanup()


def set_white_point(r, g, b):
    """Set the white point.

    :param r: Red amount, from 0.0 to 1.0
    :param g: Green amount, from 0.0 to 1.0
    :param b: Green amount, from 0.0 to 1.0

    """
    global _white_point
    _white_point = (r, g, b)


def _set_gamma_table(table):
    """Set the gamma table.

    :param table: Must be a list of 256 values

    """

    global _gamma_table
    if isinstance(table, list) and len(table) == 256:
        _gamma_table = table


def configure_channel(channel, num_pixels, gamma_correction=False):
    """Configure a channel.

    :param channel: Index of channel to configure
    :param num_pixels: Number of pixels in channel
    :param gamma_correction: Whether this channel should be gamma corrected

    """

    global channels
    channels[channel - 1] = (num_pixels, gamma_correction)


def get_pixel_count(channel):
    """Get the number of pixels in a channel.

    :param channel:  Index of channel to query

    """

    return channels[channel - 1][0]


def set_brightness(brightness):
    """Set the brightness of all pixels

    :param brightness: Brightness: 0.0 to 1.0
    """
    for c in range(NUM_CHANNELS):
        for x in range(NUM_PIXELS_PER_CHANNEL):
            pixels[c][x][3] = brightness


def clear_channel(channel):
    """Clear a single channel

    :param channel: Channel to clear: 0 to 3
    """
    for index in range(NUM_PIXELS_PER_CHANNEL):
        pixels[channel - 1][index][0:3] = [0, 0, 0]


def clear():
    """Clear the pixel buffer"""
    for channel in range(1, NUM_CHANNELS + 1):
        clear_channel(channel)


def _select_channel(channel):
    for x in range(NUM_CHANNELS):
        GPIO.output(CHANNEL_PINS[x], GPIO.LOW if x == channel else GPIO.HIGH)


def _write_byte(byte):
    for x in range(8):
        GPIO.output(DAT_PIN, byte & 0b10000000)
        GPIO.output(CLK_PIN, 1)
        time.sleep(_sleep_time)
        byte <<= 1
        GPIO.output(CLK_PIN, 0)
        time.sleep(_sleep_time)


# Emit exactly enough clock pulses to latch the small dark die APA102s which are weird
# for some reason it takes 36 clocks, the other IC takes just 4 (number of pixels/2)
def _eof():
    GPIO.output(DAT_PIN, 0)
    for x in range(42):
        GPIO.output(CLK_PIN, 1)
        time.sleep(_sleep_time)
        GPIO.output(CLK_PIN, 0)
        time.sleep(_sleep_time)


def _sof():
    GPIO.output(DAT_PIN, 0)
    for x in range(32):
        GPIO.output(CLK_PIN, 1)
        time.sleep(_sleep_time)
        GPIO.output(CLK_PIN, 0)
        time.sleep(_sleep_time)


def show():
    """Output the buffer to Mote pHAT"""
    global _gpio_setup

    if not _gpio_setup:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup([DAT_PIN, CLK_PIN], GPIO.OUT)
        GPIO.setup(CHANNEL_PINS, GPIO.OUT)
        atexit.register(_exit)
        _gpio_setup = True

    for index, channel in enumerate(pixels):
        _select_channel(index)
        gamma = _gamma_table if channels[1] else range(256)
        _sof()
        for pixel in channel:
            r, g, b, brightness = pixel
            r, g, b = [int(gamma[int(x)] * brightness * _white_point[i]) & 0xff for i, x in enumerate([r, g, b])]
            _write_byte(LED_SOF | LED_MAX_BR)
            _write_byte(b)
            _write_byte(g)
            _write_byte(r)

        _eof()


def set_all(r, g, b, brightness=None, channel=None):
    """Set the RGB value and optionally brightness of all pixels

    If you don't supply a brightness value, the last value set for each pixel be kept.

    :param r: Amount of red: 0 to 255
    :param g: Amount of green: 0 to 255
    :param b: Amount of blue: 0 to 255
    :param brightness: Brightness: 0.0 to 1.0 (default around 0.2)
    :param channel: Optional channel: 1, 2, 3 or 4 (default to all)

    """

    if channel in range(1, NUM_CHANNELS + 1):
        for index in range(get_pixel_count(channel)):
            set_pixel(channel, index, r, g, b, brightness)
        return

    for channel in range(1, NUM_CHANNELS + 1):
        for index in range(get_pixel_count(channel)):
            set_pixel(channel, index, r, g, b, brightness)


def get_pixel(channel, index):
    return tuple(pixels[channel - 1][index])


def set_pixel(channel, index, r, g, b, brightness=None):
    """Set the RGB value, and optionally brightness, of a single pixel

    If you don't supply a brightness value, the last value will be kept.

    :param channel: The channel on which to set the pixel: 1, 2, 3 or 4
    :param index: The horizontal position of the pixel: 0 to 7
    :param r: Amount of red: 0 to 255
    :param g: Amount of green: 0 to 255
    :param b: Amount of blue: 0 to 255
    :param brightness: Brightness: 0.0 to 1.0 (default around 0.2)

    """

    channel -= 1
    channel %= NUM_CHANNELS
    index %= get_pixel_count(channel)

    if brightness is None:
        brightness = pixels[channel][index][3]

    pixels[channel][index] = [r, g, b, brightness]


def set_clear_on_exit(value=True):
    """Set whether Mote pHAT should be cleared upon exit

    By default Mote pHAT will turn off the pixels on exit, but calling::

        blinkt.set_clear_on_exit(False)

    Will ensure that it does not.

    :param value: True or False (default True)
    """
    global _clear_on_exit
    _clear_on_exit = value
