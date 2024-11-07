import schedule
import os
import time

from dotenv import load_dotenv
from pushbullet import Pushbullet

load_dotenv()

# Pushbullet APIキー
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

# Pushbulletのインスタンスを作成
pb = Pushbullet(ACCESS_TOKEN)

def task_reminder(task):
    pb.push_note("今日のタスク", task)

# 毎朝8時にリマインダーをセット
schedule.every().day.at("23:55").do(lambda: task_reminder("今日もスクワット30回だ！"))

while True:
    schedule.run_pending()
    time.sleep(1)

