import asyncio
import discord
import os
import schedule
import time

from dotenv import load_dotenv
from google_calendar_api import GoogleCalendarAPI

load_dotenv()

GOOGLE_CALENDAR_ID = os.environ.get('GOOGLE_CALENDAR_ID')
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
DISCORD_NOTIFICATION_CHANNEL_ID = int(os.environ.get('DISCORD_NOTIFICATION_CHANNEL_ID'))

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

def create_daily_notification():
    """
    翌日のGoogleカレンダーのイベント情報を取得し、通知メッセージを作成します。

    Returns:
        str: 翌日のイベント情報を含むメッセージ。イベントがない場合は空の文字列を返します。
    """
    gc = GoogleCalendarAPI()
    events = gc.list_events_next_day(calendar_id=GOOGLE_CALENDAR_ID)
    message = ''

    if events:
        message = f'明日 {events[0]["start"].get("date")} のおしらせです🐾\n\n'
        for event in events:
            message += f'■ {event["summary"]}\n'
            if 'description' in event:
                message += f'{event["description"]}\n'
    return message

async def send_daily_notification():
    """
    指定されたDiscordチャンネルに通知メッセージを送信します。
    """
    message = create_daily_notification()
    channel = bot.get_channel(DISCORD_NOTIFICATION_CHANNEL_ID)
    if channel and message:
        await channel.send(message)

def run_schedule():
    """
    `schedule`モジュールを使用してスケジュールされたタスクを実行します。
    """
    while True:
        schedule.run_pending()
        time.sleep(60)

@bot.event
async def on_ready():
    """
    ボットが準備完了したときに呼び出されるイベントハンドラ。
    `send_daily_notification` 関数を毎日20時に実行するようにスケジュールを設定します。
    """
    print(f'{bot.user} Ready')
    # 毎日20時にお知らせを送信
    schedule.every().day.at("02:50").do(lambda: asyncio.run_coroutine_threadsafe(send_daily_notification(), bot.loop))

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_schedule, daemon=True).start()
    bot.run(DISCORD_TOKEN)
