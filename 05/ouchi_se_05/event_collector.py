import json
import os
import re
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL_FOR_EVENT_COLLECTOR = os.environ.get("OPENAI_MODEL_FOR_EVENT_COLLECTOR", "gpt-4o")
urls = os.environ.get("URLS", [])

if urls:
    urls = json.loads(urls)

def fetch_html_contents(url):
  response = requests.get(url)

  # HTMLコンテンツをパース
  soup = BeautifulSoup(response.content, "html.parser")

  # 全てのテキストを抽出
  text = soup.get_text()

  # 余分な空白を取り除き、改行する
  cleaned_text = '\n'.join(text.split())

  return cleaned_text

def parse_date(str):
    matches = re.findall(r"(\d+)年(\d+)月(\d+)日", str)
    year, month, day = matches[0]
    return f'{year}-{month}-{day}'

def format_data(text):
    # 正規表現パターンの定義
    pattern = r"- イベント名: (.+?)\n\s*- 開始日: (.+?)\n\s*- 終了日: (.+?)\n\s*- 会場: (.+?)\n\s*- 詳細: (.+?)\n"
    # 正規表現でテキストから情報を抽出
    matches = re.findall(pattern, text, re.DOTALL)
    
    # 抽出した情報を辞書型に格納し、リストに追加
    events = []
    for match in matches:
        if len(match) >= 5:
            # 日付をiso形式に変更する
            start_datetime = parse_date(match[1])
            end_datetime = parse_date(match[2])
            title = match[0]
            location = match[3]
            details = match[4]

            events.append({
              "イベント名": title,
              "開始日": start_datetime,
              "終了日": end_datetime,
              "会場": location,
              "詳細": details
            })
    
    return events

def extract_event_info(text):
  system_prompt = """
      あなたは文書からデータを抽出するbotです。
      以下のフォーマットに沿って、ユーザーが提示する文書から、各イベントごとに「イベント名」「開始日」「終了日」「会場」「詳細」を抽出してください。
      全てのイベントを抽出してください。余計な文章を前後につける必要はありません。

      出力例:
      - イベント名: 世界民族音楽フェスティバル2024
      - 開始日: 2024年9月5日
      - 終了日: 2024年9月10日
      - 会場: 音風文化ホール
      - 詳細: https://www.otokaze-worldmusic.jp/2024

      - イベント名: ロボテック・エクスポ2024
      - 開始日: 2024年11月3日
      - 終了日: 2024年11月10日
      - 会場: 未来創造センター
      - 詳細: https://www.robotex-futureexpo.jp/events/robotech_expo2024

      """
  openai_client = OpenAI(api_key=OPENAI_API_KEY)
  response = openai_client.chat.completions.create(
      model=OPENAI_MODEL_FOR_EVENT_COLLECTOR,
      messages=[
          {
              "role": "system",
              "content": [
                  {
                      "type": "text",
                      "text": system_prompt,
                  }
              ]
          },
          {
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text": text
                  }
              ]
          },
      ],
      temperature=1,
      max_tokens=4096,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
  )

  return response.choices[0].message.content

if __name__ == "__main__":
    # 各URLごとにコンテンツの取得・情報の抽出処理を実行
    for url in urls:
        html_contents = fetch_html_contents(url)
        event_info = extract_event_info(html_contents)
        result = format_data(event_info)
        print(result)
