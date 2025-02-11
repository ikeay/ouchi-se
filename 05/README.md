# 【おうちSEになろう！】おうちSEになって、我が家をアップデートする！
連載へのリンクはこちら
 [【おうちSEになろう！】自動で情報を収集するAIプログラムをかこう](https://www.altx.co.jp/careetec/magazine/column/ikezawa-home-se5/)

## 環境
- Python 3.12
- Poetry: パッケージ管理ツール

## セットアップ
環境変数用のファイルをコピーして、設定が必要な項目を .env ファイルに設定してください。
Open AIのAPI Key、使用するモデル、スクレイピングしたいURL（配列）を記載してください。

```bash
cp env.example .env
```

プロジェクトのディレクトリに移動し、pyproject.tomlに基づいて依存関係をインストールします。

```bash
poetry install
```

仮想環境をアクティブにするには、以下のコマンドを使用します。
poetry のバージョンが2.0以降の場合は、`poetry shell` ではなく、 `poetry env activate` を使用してください。
実行時に表示される source コマンドも実行してください。

```bash
poetry shell
```

プログラムを実行
```bash
python ouchi_se_05/event_collector.py
```

プログラムを途中で止めるときは `Ctrl + C` で止めてください。
