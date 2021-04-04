from threading import Timer as defer
from dateutil import parser as date_parser, tz as time_zones
from datetime import datetime, timedelta
from functools import partial
from math import floor, log
from house_elves.calendar_fetcher import CalendarFetcher
from house_elves.binary_presenters import get_presenter


class RememberAll:
	def __init__(
		self,
		calendars,
		slot_count=50,
		seconds_considered=24*60*60*7,
		credentials_path='service-account.json',
	):
		self.calendars = calendars
		self.slot_count = slot_count
		self.seconds_considered = seconds_considered
		self.credentials_path = credentials_path
		self.data_presenter = get_presenter(led_count=slot_count)
		self.last_fetch_attempt = None
		self.most_recent_presentation = None
		self.events = {}

	def tick(self):
		time_zero = datetime.now(tz=time_zones.UTC)
		defer(0.001, partial(self.update_events, time_zero)).start()
		defer(0.001, partial(self.update_presentation, time_zero)).start()

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
			seconds_considered=self.seconds_considered,
			slot_count=self.slot_count
		)
		if event_slots != self.most_recent_presentation:
			self.most_recent_presentation = event_slots
			self.data_presenter(event_slots)

	@staticmethod
	def calculate_perspective_slots(
		time_zero,
		events,
		seconds_considered,
		slot_count,
	):
		slots = [False] * slot_count
		for event in events:
			event_perspective = RememberAll.calculate_event_perspective(
				event=event,
				seconds_considered=seconds_considered,
				time_zero=time_zero,
				slot_count=slot_count
			)
			if event_perspective is not None and 0 <= event_perspective < slot_count:
				slots[event_perspective] = True
		return slots

	@staticmethod
	def calculate_event_perspective(
		event,
		time_zero,
		slot_count,
		seconds_considered,
	):
		base = (seconds_considered+1)**(1/slot_count)
		start = event['start']
		zulu = 'T00:00:00Z'
		event_start = start.get('dateTime') or start.get('date') + zulu
		from_now = date_parser.isoparse(event_start) - time_zero
		try:
			return floor(log(from_now.total_seconds() + 1, base))
		except ValueError:
			return None
