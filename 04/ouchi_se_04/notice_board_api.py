from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from PIL import Image

import base64
import cairosvg
import httpx
import os
import io

from ouchi_se_04.google_calendar_api import GoogleCalendarAPI

app = FastAPI()

# 東京都の地域コード
CITY_CODE = "130010"

load_dotenv()
GOOGLE_CALENDAR_ID = os.environ.get('GOOGLE_CALENDAR_ID')
GOOGLE_CALENDAR_CREDENTIAL_PATH = os.environ.get('GOOGLE_CALENDAR_CREDENTIAL_PATH')

@app.get("/api/notice_board")
async def read_root():
    events = await get_google_calendar_events()
    weather = await get_today_weather()
    return {"events": events, "weather": weather}

@app.get("/api/notice_board/google_calendar_events")
async def get_google_calendar_events():
    try:
        gc = GoogleCalendarAPI()
        events = gc.list_events_today(calendar_id=GOOGLE_CALENDAR_ID)
        summary = []
        if events:
            for event in events:
                summary.append(event['summary'])

        return {"events": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notice_board/weather")
async def get_today_weather():
    try:
        # Tsukumijima APIへのリクエスト
        url = f"http://weather.tsukumijima.net/api/forecast/city/{CITY_CODE}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # ステータスコードが200以外なら例外を発生

        data = response.json()

        # 今日の天気データを抽出
        today_forecast = data["forecasts"][0]

        # SVG画像を取得
        async with httpx.AsyncClient() as client:
            svg_response = await client.get(today_forecast["image"]["url"])
            svg_response.raise_for_status()

        # SVG画像をbytearrayに変換
        bitmap = svg_to_bitmap(svg_response.content, 80, 80)
        bitmap_base64 = base64.b64encode(bitmap).decode('utf-8')

        weather = {
            "location": data["location"]["city"],  # 地域名
            "date": today_forecast["date"],        # 日付
            "weather": today_forecast["telop"],    # 天気
            "weather_image": today_forecast["image"]["url"],  # 天気画像のURL
            "weather_image_bitmap": bitmap_base64,  # 天気画像のバイナリデータ
            "temperature": {
                "min": today_forecast["temperature"]["min"]["celsius"] if today_forecast.get("temperature") and today_forecast["temperature"]["min"] else None,
                "max": today_forecast["temperature"]["max"]["celsius"] if today_forecast.get("temperature") and today_forecast["temperature"]["max"] else None,
            },
        }
        return weather

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch weather data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def svg_to_bitmap(svg_data, output_width, output_height):
    """
    SVG画像をモノクロビットマップに変換する関数。

    Parameters:
    - svg_data: SVGのバイトデータ
    - output_width: 出力画像の幅
    - output_height: 出力画像の高さ

    Returns:
    - bitmap: モノクロビットマップ画像（bytearray形式）
    """
    # SVGをPNGバイナリに変換
    png_data = cairosvg.svg2png(bytestring=svg_data, output_width=output_width, output_height=output_height)

    # PNGをPillowで読み込み
    with Image.open(io.BytesIO(png_data)) as img:
        # モノクロ（1ビット）に変換
        img = img.convert("1")

        # バイナリビットマップ形式に変換
        bitmap = bytearray(img.tobytes())

    return bitmap
