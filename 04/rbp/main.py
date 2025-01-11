# *****************************************************************************
# * | File        :	  Pico_ePaper-2.13-B_V4.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2022-08-22
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import framebuf
import network
import sys
import time
import urequests as requests
import utime

from machine import Pin, SPI
from misakifont import MisakiFont

import binascii
import json
import ubinascii
from machine import Pin, SPI
import framebuf

EPD_WIDTH       = 122
EPD_HEIGHT      = 250

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

class EPD_2in13_B_V4_Portrait:
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        if EPD_WIDTH % 8 == 0:
            self.width = EPD_WIDTH
        else :
            self.width = (EPD_WIDTH // 8) * 8 + 8
        self.height = EPD_HEIGHT
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
        
        
        self.buffer_balck = bytearray(self.height * self.width // 8)
        self.buffer_red = bytearray(self.height * self.width // 8)
        self.imageblack = framebuf.FrameBuffer(self.buffer_balck, self.width, self.height, framebuf.MONO_HLSB)
        self.imagered = framebuf.FrameBuffer(self.buffer_red, self.width, self.height, framebuf.MONO_HLSB)
        self.init()

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)

    # Hardware reset
    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)


    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)
        
    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)
        
    def ReadBusy(self):
        print('busy')
        while(self.digital_read(self.busy_pin) == 1): 
            self.delay_ms(10) 
        print('busy release')
        self.delay_ms(20)
        
    def TurnOnDisplay(self):
        self.send_command(0x20)  # Activate Display Update Sequence
        self.ReadBusy()

    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        self.send_command(0x44) # SET_RAM_X_ADDRESS_START_END_POSITION
        self.send_data((Xstart>>3) & 0xFF)
        self.send_data((Xend>>3) & 0xFF)

        self.send_command(0x45) # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(Ystart & 0xFF)
        self.send_data((Ystart >> 8) & 0xFF)
        self.send_data(Yend & 0xFF)
        self.send_data((Yend >> 8) & 0xFF)
        
    def SetCursor(self, Xstart, Ystart):
        self.send_command(0x4E) # SET_RAM_X_ADDRESS_COUNTER
        self.send_data(Xstart & 0xFF)

        self.send_command(0x4F) # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(Ystart & 0xFF)
        self.send_data((Ystart >> 8) & 0xFF)
    

    def init(self):
        print('init')
        self.reset()
        
        self.ReadBusy()   
        self.send_command(0x12)  #SWRESET
        self.ReadBusy()   

        self.send_command(0x01) #Driver output control      
        self.send_data(0xf9)
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x11) #data entry mode       
        self.send_data(0x03)

        self.SetWindows(0, 0, self.width-1, self.height-1)
        self.SetCursor(0, 0)

        self.send_command(0x3C) #BorderWaveform
        self.send_data(0x05)

        self.send_command(0x18) #Read built-in temperature sensor
        self.send_data(0x80)

        self.send_command(0x21) #  Display update control
        self.send_data(0x80)
        self.send_data(0x80)

        self.ReadBusy()
        
        return 0       
        
    def display(self):
        self.send_command(0x24)
        self.send_data1(self.buffer_balck)
        
        self.send_command(0x26)
        self.send_data1(self.buffer_red)  

        self.TurnOnDisplay()

    
    def Clear(self, colorblack, colorred):
        self.send_command(0x24)
        self.send_data1([colorred] * self.height * int(self.width / 8))
        
        self.send_command(0x26)
        self.send_data1([colorred] * self.height * int(self.width / 8))
                                
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x10) 
        self.send_data(0x01)
        
        self.delay_ms(2000)
        self.module_exit()
        
class EPD_2in13_B_V4_Landscape:
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        if EPD_WIDTH % 8 == 0:
            self.width = EPD_WIDTH
        else :
            self.width = (EPD_WIDTH // 8) * 8 + 8
        self.height = EPD_HEIGHT
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
        
        
        self.buffer_balck = bytearray(self.height * self.width // 8)
        self.buffer_red = bytearray(self.height * self.width // 8)
        self.imageblack = framebuf.FrameBuffer(self.buffer_balck, self.height, self.width, framebuf.MONO_VLSB)
        self.imagered = framebuf.FrameBuffer(self.buffer_red, self.height, self.width, framebuf.MONO_VLSB)
        self.init()

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)

    # Hardware reset
    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)


    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)
        
    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)
        
    def ReadBusy(self):
        print('busy')
        while(self.digital_read(self.busy_pin) == 1): 
            self.delay_ms(10) 
        print('busy release')
        self.delay_ms(20)
        
    def TurnOnDisplay(self):
        self.send_command(0x20)  # Activate Display Update Sequence
        self.ReadBusy()

    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        self.send_command(0x44) # SET_RAM_X_ADDRESS_START_END_POSITION
        self.send_data((Xstart>>3) & 0xFF)
        self.send_data((Xend>>3) & 0xFF)

        self.send_command(0x45) # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(Ystart & 0xFF)
        self.send_data((Ystart >> 8) & 0xFF)
        self.send_data(Yend & 0xFF)
        self.send_data((Yend >> 8) & 0xFF)
        
    def SetCursor(self, Xstart, Ystart):
        self.send_command(0x4E) # SET_RAM_X_ADDRESS_COUNTER
        self.send_data(Xstart & 0xFF)

        self.send_command(0x4F) # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(Ystart & 0xFF)
        self.send_data((Ystart >> 8) & 0xFF)
    

    def init(self):
        print('init')
        self.reset()
        
        self.ReadBusy()   
        self.send_command(0x12)  #SWRESET
        self.ReadBusy()   

        self.send_command(0x01) #Driver output control      
        self.send_data(0xf9)
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x11) #data entry mode       
        self.send_data(0x07)

        self.SetWindows(0, 0, self.width-1, self.height-1)
        self.SetCursor(0, 0)

        self.send_command(0x3C) #BorderWaveform
        self.send_data(0x05)

        self.send_command(0x18) #Read built-in temperature sensor
        self.send_data(0x80)

        self.send_command(0x21) #  Display update control
        self.send_data(0x80)
        self.send_data(0x80)

        self.ReadBusy()
        
        return 0       
        
    def display(self):
        self.send_command(0x24)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(self.buffer_balck[i + j * self.height])
        
        self.send_command(0x26)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(self.buffer_red[i + j * self.height])

        self.TurnOnDisplay()

    
    def Clear(self, colorblack, colorred):
        self.send_command(0x24)
        self.send_data1([colorblack] * self.height * int(self.width / 8))
        
        self.send_command(0x26)
        self.send_data1([colorred] * self.height * int(self.width / 8))
                                
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x10) 
        self.send_data(0x01)
        
        self.delay_ms(2000)
        self.module_exit()

def jpblackchar(fd, epd, x, y):
    for row in range(0,7):
        for col in range(0,7):
            if (0x80>>col) & fd[row]:
                epd.imageblack.pixel(col + x, row + y, 0x00)

def jpblacktext(str, x, y, mf, epd):
    str = replace_unsupported_char(str)
    for c in str:
        d = mf.font(ord(c))
        jpblackchar(d, epd, x, y)
        x = x + 9

def replace_unsupported_char(str):
    str = str.replace("曇", "くもり")
    str = str.replace("-", "−") # ハイフンが表示できないのでマイナス記号に変換
    return str

def connect_to_wifi_old(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        time.sleep(1)
        print("Connecting to WiFi...")
        max_wait -= 1
    if wlan.status() != 3:
        raise RuntimeError("Failed to connect to WiFi")
    else:
        print("Connected to WiFi")
        status = wlan.ifconfig()
        print("IP Address: ", status[0])

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)  # Wi-Fiを有効化

    wlan.connect(ssid, password)
    max_wait = 20  # タイムアウト秒数

    while max_wait > 0:
        status = wlan.status()
        if status < 0 or status >= 3:  # エラーまたは成功
            break
        print("Connecting to WiFi...")
        time.sleep(1)
        max_wait -= 1

    # ステータスに応じて処理
    if wlan.status() != 3:
        print("WiFi connection failed")
        print(f"WiFi status: {wlan.status()}")
        raise RuntimeError("Failed to connect to WiFi")
    else:
        print("Connected to WiFi")
        print(f"IP Address: {wlan.ifconfig()[0]}")

def run_main_process():
    # フォントの読み込み
    mf = MisakiFont()

    # 電子ペーパーの初期化
    epd = EPD_2in13_B_V4_Landscape()
    epd.Clear(0xff, 0xff)
    epd.imageblack.fill(0xff)

    # ネットワークに接続
    ssid = "ssid" # SSIDを自宅のものに書き換える
    password = "password" # パスワードを自宅のものに書き換える

    try:
        connect_to_wifi(ssid, password)
    except Exception as e:
        print("Error: ", e)
        jpblacktext("Wi-Fi接続に失敗しましたあ！", 12, 10, mf, epd)
        epd.display()
        epd.sleep()
        return

    # APIからデータを取得
    url = "http://192.168.1.100:8000/api/notice_board" # IPアドレスは適宜書き換える
    data = None

    try:
        response = requests.get(url, timeout=120)
        print("ステータスコード:", response.status_code)  # HTTPステータスコード
        print("レスポンスヘッダー:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")  # レスポンスヘッダーを表示
        print("レスポンスボディ:")
        print(response.text)  # レスポンスの本文（文字列として取得）
        if response.status_code == 200:
            data = json.loads(response.text)
        else:
            raise RuntimeError("Failed to get data from server")
    except Exception as e:
        print("Error: ", e)
        jpblacktext("データが取得できませんでした。", 12, 10, mf, epd)
        epd.display()
        epd.sleep()
        return

    finally:
        # リソースを解放
        if 'response' in locals():
            response.close()

    # データを電子ペーパーに表示する
    if data:
        location = data["weather"]["location"]
        date = data["weather"]["date"]
        weather_description = data["weather"]["weather"]
        min_temp = data["weather"]["temperature"]["min"]
        max_temp = data["weather"]["temperature"]["max"]
        events = data["events"]["events"]
        bitmap_base64 = data["weather"]["weather_image_bitmap"]

        # Base64デコードしてビットマップデータを取得
        bitmap_data = ubinascii.a2b_base64(bitmap_base64)

        # テキスト描画
        text_x = 110
        y = 12
        jpblacktext(f"場所: {location}", text_x, y, mf, epd)
        y += 12
        jpblacktext(f"日付: {date}", text_x, y, mf, epd)
        y += 12
        jpblacktext(f"天気: {weather_description}", text_x, y, mf, epd)
        y += 12
        jpblacktext(f"最低: {min_temp}°C", text_x, y, mf, epd)
        y += 12
        jpblacktext(f"最高: {max_temp}°C", text_x, y, mf, epd)
        y += 12
        jpblacktext("イベント:", text_x, y, mf, epd)
        y += 12
        for event in events:
            jpblacktext(f"- {event}", text_x, y, mf, epd)
            y += 12

        # ビットマップ画像の描画
        bitmap_width = 80  # 画像幅
        bitmap_height = 80  # 画像高さ
        bitmap_x = 10  # 画像のX座標
        bitmap_y = 10  # 画像のY座標

        # Base64デコード
        bitmap = binascii.a2b_base64(bitmap_base64)

        # 1行に含まれるバイト数
        bytes_per_row = (bitmap_width + 7) // 8  # 8ピクセルを1バイトとして計算

        # 各ピクセルを描画
        for y in range(bitmap_height):
            for x in range(bitmap_width):
                # 現在のピクセルが格納されているバイトとビットの位置を計算
                byte_index = y * bytes_per_row + (x // 8)  # 行ごとにオフセット計算
                bit_index = 7 - (x % 8)  # 左から右へのビット位置

                # ピクセル値を取得（0: 黒, 1: 白）
                pixel_value = (bitmap[byte_index] >> bit_index) & 1

                # 白黒を反転（1: 黒, 0: 白）
                inverted_pixel_value = 1 - pixel_value

                # ePaperディスプレイに描画
                epd.imageblack.pixel(bitmap_x + x, bitmap_y + y, inverted_pixel_value)

    # フレームバッファを電子ペーパーに転送
    epd.display()

    # スリープモード
    epd.sleep()


if __name__=='__main__':
    while True:
        run_main_process()
        time.sleep(60 * 60) # 1時間ごとに更新