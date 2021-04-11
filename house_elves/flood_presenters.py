from math import floor, ceiling


class NeopixelPresenter:
	def __init__(
		self,
		led_count=50,
		led_pin=18,
		led_freq=800000,
		led_dma=10,
		led_invert=False,
		led_brightness=255,
		led_channel=0,
	):
		from rpi_ws281x import PixelStrip
		self.led_count = led_count
		self.led_strip = PixelStrip(
			led_count, led_pin, led_freq, led_dma,
			led_invert, led_brightness, led_channel,
		)
		self.led_strip.begin()

	def present(self, value):
		"""Present a value flood filling NeoPixel array"""
		from rpi_ws281x import Color as Colour
		fraction = value % 1
		for i in range(self.led_count):
			if i / self.led_count < fraction:
				brightness = ceiling(value)
			else:
				brightness = floor(value)
			color = Color(brightness, brightness, brightness)
			led_strip.setPixelColor(i, color)
		led_strip.show()


def terminal_presenter(value):
	"""Present a value on a single console line"""
	output = ':' + value + ':'
	print(output)


def get_presenter(led_count=50):
	"""Get the prettiest function available for presenting a value"""
	try:
		neopixel_presenter = NeopixelPresenter(led_count)
		return neopixel_presenter.present
	except ModuleNotFoundError:
		return terminal_presenter
