# 【おうちSEになろう！】おうちSEになって、我が家をアップデートする！
連載へのリンクはこちら
 [【おうちSEになろう！】Raspberry Pi で遊ぼう](https://www.altx.co.jp/careetec/magazine/column/ikezawa-home-se3/)

※注意: この回は、主に Raspberry Pi の設定やプログラムの実行方法について触れています。hello.py も cron の実行のテスト用に実装したものなので、シンプルなプログラムになっています。

## 環境
- Python 3.12
- Poetry: パッケージ管理ツール

## セットアップ
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
python ouchi_se_03/hello.py
```

プログラムを途中で止めるときは `Ctrl + C` で止めてください。
