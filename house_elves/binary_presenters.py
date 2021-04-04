def terminal_presenter(data):
	"""Present a binary array on a single console line"""
	output = ':'
	for datum in data:
		output += '*' if datum else ' '
	print(output)


def neopixel_presenter(
	data,
	led_count=24,
	led_pin=18,
	led_freq=800000,
	led_dma=10,
	led_invert=False,
	led_brightness=32,
	led_channel=0,
):
	"""Present a binary array as illuminated dots on a NeoPixel array"""
	from rpi_ws281x import PixelStrip, Color as Colour
	from math import floor
	led_strip = PixelStrip(
		led_count, led_pin, led_freq, led_dma,
		led_invert, led_brightness, led_channel,
	)
	led_strip.begin()
	for (index, datum) in enumerate(data):
		# Far-away events should be in a calming colour
		# So as the index approaches the maximum index, the blueness maxes out
		blueness = (index * 255) / (led_count - 1)
		blue = floor(blueness)
		# Near-to events should be in an alerting colour
		red = floor(255-blueness)
		# The LED should be illuminated on a truthy value
		colour = Colour(red, 0, blue) if datum else Colour(0, 0, 0)
		led_strip.setPixelColor(index, colour)
	led_strip.show()
