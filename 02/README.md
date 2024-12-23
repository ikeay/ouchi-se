# 【おうちSEになろう！】おうちSEになって、我が家をアップデートする！
連載へのリンクはこちら
 [【おうちSEになろう！】おうちチャットで動くBotをつくる](https://www.altx.co.jp/careetec/magazine/column/ikezawa-home-se2/)

## 環境
- Python 3.12
- Poetry: パッケージ管理ツール

## セットアップ
環境変数用のファイルをコピーして、設定が必要な項目を .env ファイルに設定してください。
詳しい設定方法等は連載記事に記述しています。

```bash
cp env.example .env
```

Google Calendar APIも使用するので `credentials.json` を取得し、 `ouchi-se/02/ouchi_se_02/` のディレクトリに置いてください。
詳しい設定方法等は連載記事に記述しています。


プロジェクトのディレクトリに移動し、pyproject.tomlに基づいて依存関係をインストールします。

```bash
poetry install
```

仮想環境をアクティブにするには、以下のコマンドを使用します。
```bash
poetry shell
```

プログラムを実行
```bash
python ouchi_se_02/notification_daily.py
```

プログラムを途中で止めるときは `Ctrl + C` で止めてください。
