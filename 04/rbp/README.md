# 【おうちSEになろう！】玄関に置くデジタルお知らせボードをつくる
Raspberry Pi Pico に書き込むお知らせボードのプログラム。Googleカレンダーに登録しているお知らせ情報と天気情報を電子ペーパーに表示する。

## プログラム
- main.py: お知らせボード用プログラム
- clear.py: 画面をクリアするためのプログラム

## 仕様
- MicroPython
- MisakiFont で日本語対応

## プログラム使用の際の注意点
  - 日本語の表示には以下のプロジェクトを利用。Raspberry Pi Pico にフォントをアップロードして使う。
    - https://github.com/Tamakichi/pico_MicroPython_misakifont
  - プログラム内の wifi, password を自宅のものに書き換える。
  - Raspberry Pi Zero などにデプロイした API の IP アドレスに、プログラム内の IP アドレスを書き換える。
