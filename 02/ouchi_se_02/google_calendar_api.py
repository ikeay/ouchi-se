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

    def list_events_next_day(self, calendar_id='primary'):
        """
        指定されたカレンダーの翌日のイベントを取得します。

        Args:
            calendar_id (str): イベントを取得するカレンダーのID。デフォルトは 'primary'。

        Returns:
            list: 翌日に発生するイベントのリスト。
        """
        t_delta = datetime.timedelta(hours=9) # 日本標準時 (JST) のタイムゾーンオフセット
        JST = datetime.timezone(t_delta, 'JST')
        # 翌日の0時から始まる時間範囲を設定
        time_min = datetime.datetime.now(JST).replace(hour=0, minute=0, second=0) + datetime.timedelta(days=1)
        time_max = time_min + datetime.timedelta(days=1)
        # イベントを取得
        events_result = self.service.events().list(
            calendarId=calendar_id, timeMin=time_min.isoformat(), timeMax=time_max.isoformat(), singleEvents=True, orderBy='startTime'
        ).execute()
        return events_result.get('items', [])

# GoogleCalendarAPIクラスの使用例
if __name__ == "__main__":
    gc = GoogleCalendarAPI()
    events = gc.list_events_next_day(calendar_id=GOOGLE_CALENDAR_ID)

    if events:
        for event in events:
            print(event['start'].get('dateTime', event['start'].get('date')))
            print(event['summary'])
            print(event.get('description'))
            print('---')