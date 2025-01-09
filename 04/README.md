# 【おうちSEになろう！】玄関に置くデジタルお知らせボードをつくる
連載へのリンクはこちら
 [【おうちSEになろう！】玄関に置くデジタルお知らせボードをつくる](https://www.altx.co.jp/careetec/magazine/column/ikezawa-home-se4/)

## バックエンドAPI
### 環境
- Python 3.12
- Poetry: パッケージ管理ツール
- Fast　API: 使用フレームワーク

### セットアップ
環境変数用のファイルをコピーして、設定が必要な項目を .env ファイルに設定してください。
Google カレンダーのクレデンシャルの取得の仕方など、詳しい設定方法等は[以前の記事（【おうちSEになろう！】おうちチャットで動くBotをつくる）](https://www.altx.co.jp/careetec/magazine/column/ikezawa-home-se2/)を参考にしてください。

```bash
cp env.example .env
```

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
uvicorn ouchi_se_04.notice_board_api:app --host 0.0.0.0 --port 8000 --reload
```

プログラムを途中で止めるときは `Ctrl + C` で止めてください。
