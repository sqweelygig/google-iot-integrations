from threading import Timer as defer, active_count
from dateutil import parser as date_parser, tz as time_zones
from datetime import datetime, timedelta
from functools import partial
from house_elves.calendar_fetcher import CalendarFetcher
from house_elves.binary_presenters import get_presenter


class RememberAll:
	def __init__(
		self,
		calendars,
		slot_count=24,
		seconds_considered=24*60*60,
		credentials_path='service-account.json',
		smallest_slot=60,
		setup_time=0.5,
	):
		self.calendars = calendars
		self.slot_count = slot_count
		self.smallest_slot = smallest_slot
		self.credentials_path = credentials_path
		self.data_presenter = get_presenter(led_count=slot_count)
		self.last_fetch_attempt = None
		self.most_recent_presentation = None
		self.events = {}
		self.slot_growth = RememberAll.calculate_slot_growth(
			slot_count=slot_count,
			seconds_considered=seconds_considered,
			smallest_slot=smallest_slot,
			time_permitted=timedelta(seconds=setup_time),
		)
		time_zero = datetime.now(tz=time_zones.UTC)
		self.event_thread = defer(
			0.001,
			partial(self.update_events, time_zero),
		)
		self.event_thread.start()
		self.presentation_thread = defer(
			0.001,
			partial(self.update_events, time_zero),
		)
		self.presentation_thread.start()

	def tick(self):
		time_zero = datetime.now(tz=time_zones.UTC)
		if not self.event_thread.is_alive():
			self.event_thread = defer(
				0.001,
				partial(self.update_events, time_zero),
			)
			self.event_thread.start()
		else:
			print(time_zero, "Skipping calendar update.")
		if not self.presentation_thread.is_alive():
			self.presentation_thread = defer(
				0.001,
				partial(self.update_presentation, time_zero),
			)
			self.presentation_thread.start()
		else:
			print(time_zero, "Skipping presentation update.")

	def update_events(self, time_zero):
		# Throttle the API requests
		if(
			self.last_fetch_attempt is None or
			time_zero - self.last_fetch_attempt > timedelta(minutes=1)
		):
			self.last_fetch_attempt = time_zero
			events = CalendarFetcher.fetch_events(
				time_zero=time_zero,
				calendars=self.calendars,
				credentials_path=self.credentials_path,
			)
			self.events = events

	def update_presentation(self, time_zero):
		event_slots = RememberAll.calculate_perspective_slots(
			time_zero=time_zero,
			events=self.events.values(),
			smallest_slot=self.smallest_slot,
			slot_growth=self.slot_growth,
			slot_count=self.slot_count,
		)
		if event_slots != self.most_recent_presentation:
			self.most_recent_presentation = event_slots
			self.data_presenter(event_slots)

	def present_event_boundaries(self):
		seconds_done = 0.0
		for i in range(self.slot_count):
			slot_size = self.smallest_slot * (self.slot_growth**i)
			print(
				"Slot", i,
				"covers about", round(seconds_done),
				"to", round(seconds_done + slot_size),
				"seconds.",
			)
			seconds_done += slot_size
		print("This scale covers ", timedelta(seconds=seconds_done), ".", sep="")

	@staticmethod
	def calculate_perspective_slots(
		time_zero,
		events,
		smallest_slot,
		slot_growth,
		slot_count,
	):
		slots = [False] * slot_count
		for event in events:
			event_perspective = RememberAll.calculate_event_perspective(
				event=event,
				smallest_slot=smallest_slot,
				slot_growth=slot_growth,
				time_zero=time_zero,
			)
			if event_perspective is not None and 0 <= event_perspective < slot_count:
				slots[event_perspective] = True
		return slots

	@staticmethod
	def calculate_event_perspective(
		event,
		time_zero,
		smallest_slot,
		slot_growth,
	):
		start = event['start']
		zulu = 'T00:00:00Z'
		event_start = start.get('dateTime') or start.get('date') + zulu
		time_difference = (date_parser.isoparse(event_start) - time_zero)
		seconds_difference = time_difference.total_seconds()
		slot = -1
		while seconds_difference > 0:
			slot += 1
			seconds_difference -= smallest_slot * (slot_growth**slot)
		return slot

	@staticmethod
	def calculate_slot_growth(
		slot_count,
		smallest_slot,
		seconds_considered,
		time_permitted,
	):
		time_to_end = datetime.now(tz=time_zones.UTC) + time_permitted
		lower_bound = 0.0
		upper_bound = seconds_considered / smallest_slot
		test_point = (lower_bound + upper_bound) / 2.0
		while datetime.now(tz=time_zones.UTC) < time_to_end:
			seconds_covered = 0
			for i in range(slot_count):
				slot_size = smallest_slot * (test_point**i)
				seconds_covered += slot_size
			if seconds_covered > seconds_considered:
				upper_bound = test_point
			else:
				lower_bound = test_point
			test_point = (lower_bound + upper_bound) / 2.0
		return upper_bound
