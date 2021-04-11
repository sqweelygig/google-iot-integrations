from threading import Timer as defer
from dateutil import tz as time_zones
from datetime import datetime, timedelta
from functools import partial
from google.oauth2.service_account import Credentials as credentials_builder
from googleapiclient.discovery import build as service_builder


class CalendarFetcher:
	def __init__(self, calendars, credentials_path='service-account.json'):
		self.calendars = calendars
		self.credentials_path = credentials_path
		self.last_fetch_attempt = None
		self.events = {}
		time_zero = datetime.now(tz=time_zones.UTC)
		self.data_thread = defer(
			0.001,
			partial(self.update_data, time_zero),
		)
		self.data_thread.start()
		self.presentation_thread = defer(
			0.001,
			partial(self.update_presentation, time_zero),
		)
		self.presentation_thread.start()

	def tick(self):
		time_zero = datetime.now(tz=time_zones.UTC)
		if not self.data_thread.is_alive():
			self.data_thread = defer(
				0.001,
				partial(self.update_data, time_zero),
			)
			self.data_thread.start()
		else:
			print(time_zero, "Skipping data update.")
		if not self.presentation_thread.is_alive():
			self.presentation_thread = defer(
				0.001,
				partial(self.update_presentation, time_zero),
			)
			self.presentation_thread.start()
		else:
			print(time_zero, "Skipping presentation update.")

	def update_data(self, time_zero):
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
		pass

	@staticmethod
	def fetch_events(time_zero, calendars, credentials_path):
		events = {}
		for calendar in calendars:
			event_list = CalendarFetcher.fetch_event_list(
				calendar,
				credentials_path=credentials_path,
				time_zero=time_zero
			)
			for event in event_list:
				events[event.get('htmlLink')] = event
		return events

	@staticmethod
	def fetch_event_list(
		calendar,
		time_zero,
		credentials_path='service-account.json',
		scope='https://www.googleapis.com/auth/calendar.readonly',
		order_by='startTime',
	):
		credentials = credentials_builder.from_service_account_file(
			credentials_path,
			scopes=[scope],
		)
		calendar_service = service_builder('calendar', 'v3', credentials=credentials)
		return calendar_service.events().list(
			calendarId=calendar,
			orderBy=order_by,
			timeMin=time_zero.isoformat(),
			singleEvents=True
		).execute().get('items', [])
