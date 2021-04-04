from google.oauth2.service_account import Credentials as credentials_builder
from googleapiclient.discovery import build as service_builder


class CalendarFetcher():
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
