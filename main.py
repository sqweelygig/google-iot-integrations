from remember_all.remember_all import RememberAll
from time import sleep
from sys import argv as command_line_arguments

try:
	remember_all = RememberAll(
		slot_count=int(command_line_arguments[1]),
		calendars=command_line_arguments[2:],
	)
	while True:
		remember_all.tick()
		sleep(1/25)
except KeyboardInterrupt:
	pass

