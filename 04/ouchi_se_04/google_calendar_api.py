import datetime
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

load_dotenv()

GOOGLE_CALENDAR_ID = os.environ.get('GOOGLE_CALENDAR_ID')
GOOGLE_CALENDAR_CREDENTIAL_PATH = os.environ.get('GOOGLE_CALENDAR_CREDENTIAL_PATH')

class GoogleCalendarAPI:
    """
    Google カレンダー API をサービスアカウントの資格情報を使用して操作するためのクラス。
    """

    def __init__(self, credentials_path=GOOGLE_CALENDAR_CREDENTIAL_PATH, scopes=['https://www.googleapis.com/auth/calendar.readonly']):
        """
        GoogleCalendarAPI クラスのインスタンスを初期化します。

        Args:
            credentials_path (str): サービスアカウントの資格情報JSONファイルのパス。
            scopes (list): Google カレンダー API にアクセスするためのスコープのリスト。
        """
        self.credentials_path = credentials_path
        self.scopes = scopes
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """
        サービスアカウントの資格情報を使用してユーザーを認証し、Google カレンダー API サービスを設定します。
        """
        self.creds = service_account.Credentials.from_service_account_file(self.credentials_path, scopes=self.scopes)
        self.service = build('calendar', 'v3', credentials=self.creds)

    def list_events_today(self, calendar_id='primary'):
        """
        今日のカレンダーのイベントを取得します。

        Args:
            calendar_id (str): イベントを取得するカレンダーのID。デフォルトは 'primary'。

        Returns:
            list: 今日発生するイベントのリスト。
        """
        try:
            t_delta = datetime.timedelta(hours=9)
            JST = datetime.timezone(t_delta, 'JST')
            time_min = datetime.datetime.now(JST).replace(hour=0, minute=0, second=0, microsecond=0)
            time_max = datetime.datetime.now(JST).replace(hour=23, minute=59, second=59, microsecond=999999)
            time_min_iso = time_min.isoformat(timespec='microseconds')
            time_max_iso = time_max.isoformat(timespec='microseconds')

            events_result = (
                self.service.events()
                .list(
                    calendarId=calendar_id,
                    timeMin=time_min_iso,
                    timeMax=time_max_iso,
                    singleEvents=True,
                    orderBy='startTime',
                )
                .execute()
            )
            events = events_result.get('items', [])
            events = [event for event in events if 'start' in event and not 'dateTime' in event['start']]
            return events

        except Exception as e:
            print(f'GoogleCalendarAPI.list_events_today 実行時のエラー: {e}')
            return None

# GoogleCalendarAPIクラスの使用例
if __name__ == "__main__":
    gc = GoogleCalendarAPI()
    events = gc.list_events_today(calendar_id=GOOGLE_CALENDAR_ID)

    if events:
        for event in events:
            print(event['start'].get('dateTime', event['start'].get('date')))
            print(event['summary'])
            print(event.get('description'))
            print('---')