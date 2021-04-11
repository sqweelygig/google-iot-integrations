from remember_all.remember_all import RememberAll
from sleep_well.sleep_well import SleepWell
from time import sleep
from sys import argv as command_line_arguments

# TODO Add a basic CLI here
try:
	module = None
	if command_line_arguments[1] == "remember_all":
		module = RememberAll(
			led_count=int(command_line_arguments[2]),
			calendars=command_line_arguments[3:],
		)
	elif command_line_arguments[1] == "sleep_well":
		module = SleepWell(
			led_count=int(command_line_arguments[2]),
			calendars=command_line_arguments[3:],
		)
	module.present_configuration()
	while True:
		module.tick()
		sleep(1)
except KeyboardInterrupt:
	pass

