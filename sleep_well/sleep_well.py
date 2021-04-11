from house_elves.calendar_fetcher import CalendarFetcher
from house_elves.flood_presenters import get_presenter
from dateutil import parser as date_parser


class SleepWell(CalendarFetcher):
	def __init__(
		self,
		calendars,
		credentials_path='service-account.json',
		led_count=50
	):
		super().__init__(calendars=calendars, credentials_path=credentials_path)
		self.presenter = get_presenter(led_count=led_count)

	def update_presentation(self, time_zero):
		for event in self.events.values():
			SleepWell.consider_event(
				event=event,
				time_zero=time_zero,
				presenter=self.presenter
			)

	@staticmethod
	def consider_event(event, time_zero, presenter):
		zulu = 'T00:00:00Z'
		start_data = event['start']
		event_start = start_data.get('dateTime') or start_data.get('date') + zulu
		start = date_parser.isoparse(event_start)
		end_data = event['end']
		event_end = end_data.get('dateTime') or end_data.get('date') + zulu
		end = date_parser.isoparse(event_end)
		if start < time_zero < end:
			description = event.get('description')
			numbers_found = {}
			previous_word = None
			for word in regex_split('[^a-zA-Z0-9]', description):
				try:
					numbers_found[previous_word] = int(word)
				except ValueError:
					previous_word = word
			end_weight = (now - start) / (end - start)
			start_weight = 1 - end_weight
			end_level = numbers_found['to']
			start_level = numbers_found['from']
			brightness = (start_weight * start_level) + (end_weight * end_level)
			presenter(brightness)
