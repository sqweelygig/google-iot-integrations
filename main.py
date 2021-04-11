from remember_all.remember_all import RememberAll
from time import sleep
from sys import argv as command_line_arguments

# TODO Add a basic CLI here
try:
	remember_all = RememberAll(
		led_count=int(command_line_arguments[1]),
		calendars=command_line_arguments[2:],
	)
	remember_all.present_event_boundaries()
	while True:
		remember_all.tick()
		sleep(1)
except KeyboardInterrupt:
	pass

