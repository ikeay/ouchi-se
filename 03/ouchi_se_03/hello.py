from datetime import datetime
# 現在の時刻を取得
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# 時刻とメッセージを出力
print(f"{current_time} - Hello World")