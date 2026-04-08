# nemuriya-backend

## 前提条件
- `Docker`
- `Docker Compose V2`
- `make`


## 初回実行

このディレクトリで

```bash
cp example.env .env
```

必要に応じて内容を変更（example.env が更新されたタイミングで再実行が必要なことがあります）

## サーバー起動

### 初回・または一部更新時

2022/09/28 8:00以前に一度`make loc`をした場合は，dbのデータを一度削除する必要があります。その場合は，
```bash
make clean-db
```
を実行してください。また，再度`cp example.env .env`を実行してください。

### 起動方法
```bash
make loc
```

を実行すると，サーバーが起動し，アドレス一覧のサーバーへアクセスできます。

2回目以降は，`make up`を実行すると，インターネット通信無しで起動することができます。ただし最新の状態を保つためには，`make loc`を実行してください。

## linterとformatter

linterには`flake8`を，formatterには`black`を，モジュールのsortには`isort`を使用しています。

venvなどを作成して`requirements.txt`のインストールを行なった上で，VSCodeでこのディレクトリを開くと，保存時に自動的に適用されます。

例
```bash
python -m venv venv
source venv/bin/activate
pip install -U pip setuptools
pip install -r requirements.txt
code .
```

## 補足

- アドレス一覧
  - 開発サーバー: http://localhost:8000
  - Django Admin: http://localhost:8000/admin
    - email: `admin@example.com` もしくは `.env` に記載されている `ADMIN_USER`の値
    - パスワード: `admin` もしくは `.env` に記載されている `ADMIN_PASSWORD`の値
- api サーバーのシェルに入る
  ```bash
  make exec
  ```
- dbに接続
  ```bash
  make exec-db
  ```
- db など含めて，コンテナをリセットする
  ```bash
  make clean-db
  ```

## よくある質問

- `/recommends/`や`/orders/`にアクセスすると，401が返ってくる
  - まだログインしていないためです。`/signin/`にアクセスしてトークンを取得してください。
    その上で，`Authorization`ヘッダーに`Token <トークン>`を付与してください。
    adminユーザーが，デフォルトでemail: `admin@example.com`，password: `admin`で作成されています。
- 現状，`/recommends/`のAPIで，正常なリクエストを送ったはずなのにエラーが返ってくる
  - マットレスの条件で，身長159cm未満，姿勢タイプNしか実装されていないので注意してください。
