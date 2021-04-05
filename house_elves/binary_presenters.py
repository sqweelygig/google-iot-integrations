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
		self.led_strip = PixelStrip(
			led_count, led_pin, led_freq, led_dma,
			led_invert, led_brightness, led_channel,
		)
		self.led_strip.begin()

	def present(self, data):
		"""Present a binary array as illuminated dots on a NeoPixel array"""
		from rpi_ws281x import Color as Colour
		from math import floor
		for (index, datum) in enumerate(data):
			# Far-away events should be in a calming colour
			# So as the index approaches the maximum index, the blueness maxes out
			blueness = (index * 255) / (len(data) - 1)
			blue = floor(blueness)
			# Near-to events should be in an alerting colour
			red = floor(255-blueness)
			# The LED should be illuminated on a truthy value
			colour = Colour(red, 0, blue) if datum else Colour(0, 0, 0)
			self.led_strip.setPixelColor(index, colour)
		self.led_strip.show()


def terminal_presenter(data):
	"""Present a binary array on a single console line"""
	output = ':'
	for datum in data:
		output += '*' if datum else ' '
	output += ':'
	print(output)


def get_presenter(led_count=50):
	"""Get the prettiest function available for presenting a binary array"""
	try:
		neopixel_presenter = NeopixelPresenter(led_count)
		return neopixel_presenter.present
	except ModuleNotFoundError:
		return terminal_presenter
