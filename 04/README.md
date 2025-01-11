# 【おうちSEになろう！】玄関に置くデジタルお知らせボードをつくる
連載へのリンクはこちら
 [【おうちSEになろう！】玄関に置くデジタルお知らせボードをつくる](https://www.altx.co.jp/careetec/magazine/column/ikezawa-home-se4/)

## バックエンドAPI　側
### 環境
- Python 3.12
- Poetry: パッケージ管理ツール
- Fast　API: 使用フレームワーク

### セットアップ
環境変数用のファイルをコピーして、設定が必要な項目を .env ファイルに設定してください。
詳しい設定方法等は[以前の記事（【おうちSEになろう！】おうちチャットで動くBotをつくる）](https://www.altx.co.jp/careetec/magazine/column/ikezawa-home-se2/)を参考にしてください。

```bash
cp env.example .env
```

Google Calendar APIも使用するので `credentials.json` を取得し、 `ouchi-se/02/ouchi_se_02/` のディレクトリに置いてください。
詳しい設定方法等は [【おうちSEになろう！】おうちチャットで動くBotをつくる](https://www.altx.co.jp/careetec/magazine/column/ikezawa-home-se2/)に記述しています。

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
uvicorn ouchi_se_04.notice_board_api:app --host 0.0.0.0 --port 8000 --reload
```

プログラムを途中で止めるときは `Ctrl + C` で止めてください。

## 表示デバイス側
[README](./rbp/README.md) を参照
