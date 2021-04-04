from remember_all.remember_all import RememberAll
from time import sleep
from sys import argv as command_line_arguments

try:
	remember_all = RememberAll(
		command_line_arguments[2:],
		slot_count=int(command_line_arguments[1])
	)
	while True:
		remember_all.tick()
		sleep(1/25)
except KeyboardInterrupt:
	pass

