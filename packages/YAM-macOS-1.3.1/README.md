# Youtube Archive Manager

YouTube チャンネルの動画を読み込み、視聴進捗、タグ、感想、統計をまとめて管理するローカルツールです。
どの動画を見ていないのか、あの動画なんだっけ？、途中からすぐに見たい、視聴統計、配信統計を見たいという方へ

- 複数チャンネル対応
- 日本語 / English 切り替え対応
- 自動バックアップ対応
- Mac / Windows 向けワンクリック起動対応
- このフォルダ単体で配布用 Git のルートにできる構成

## 目次

- [起動方法](#起動方法)
- [配布ファイルの構成](#配布ファイルの構成)
- [ポートについて](#ポートについて)
- [初期設定](#初期設定)
- [チャンネルの入力方法](#チャンネルの入力方法)
- [YouTube API キーの取得方法](#youtube-api-キーの取得方法)
- [使い方](#使い方)
- [検索の使い方](#検索の使い方)
- [手動追加](#手動追加)
- [タグ編集](#タグ編集)
- [統計](#統計)
- [データ保存先](#データ保存先)
- [ライセンス](#ライセンス)
- [Credits](#credits)

## 起動方法

### 1. 推奨方法の場合

配布版を使う場合は、`packages/` にある zip を必ず最初に解凍してください。

重要:

- zip の中で直接起動しないでください
- 必ずフォルダごと解凍してから起動してください
- `YAM.app` や `YAM.exe` だけを単体で取り出さないでください
- 解凍されたフォルダの中身を丸ごと同じ場所に置いたまま使ってください
- `program-files/` を含めて、解凍後のフォルダ構成を崩さないでください

解凍後のフォルダ例:

- macOS: `YAM-macOS-1.3.1/`
- Windows: `YAM-Windows-1.3.1/`

その中に以下が入ります:

- 起動用アプリ
- `program-files/` フォルダ
- `README.md`
- `LICENSE`

- macOS: `YAM.app`
- Windows: `YAM.exe`

配布版は利用者の PC に Python が不要です。

起動手順:

1. zip を解凍する
2. 解凍してできた `YAM-<OS>-<version>/` フォルダを開く
3. その中の `YAM.app` または `YAM.exe` を起動する
4. `program-files/` はそのまま同じ階層に残しておく

補足:

- `program-files/` にはアプリ本体のプログラムファイル一式を同封しています
- 配布版の利用時に、通常は `program-files/` を触る必要はありません
- ただし、中身を確認したい場合や、開発・修正を行いたい場合はここを参照してください
- `program-files/` には `app.py`、`launch_yam.py`、`static/`、`templates/`、`assets/icon.png`、`tools/release/` などを同封しています

解凍の例:

- macOS: zip をダブルクリックして展開し、できたフォルダを開いて `YAM.app` を起動する
- Windows: zip を右クリックして `すべて展開` を選び、展開されたフォルダを開いて `YAM.exe` を起動する

### 2. ソース版をそのまま動かす場合

以下のランチャーを起動させてください。自動で環境構築などを行い、起動します。

- macOS: `Launch YAM.command`
- Windows: `Launch YAM.bat`

この方法は Python 3.10 以上が必要です。

### 3. 手動起動の場合

ランチャーは `launch_yam.py` を使って自動で `.venv` を作成し、必要な依存関係を入れてから起動します。

必要なもの:

- Python 3.10 以上
- 初回セットアップ時のインターネット接続

手動起動:

```bash
python launch_yam.py
```

## 配布ファイルの構成

このフォルダは、そのまま別 Git のルートとして配布管理できるようにしています。

主に使う場所:

- `packages/`
  利用者へ渡す配布用フォルダと zip
- `dist/`
  ビルド直後の実行ファイル本体
- `README.md`
  利用者向け説明
- `LICENSE`
  ライセンス情報

配布時に見る場所:

- 配布用フォルダ: `packages/YAM-<OS>-<version>/`
- 配布用 zip: `packages/YAM-<OS>-<version>.zip`
- 同封されるプログラムファイル: `packages/YAM-<OS>-<version>/program-files/`

例:

- macOS: `packages/YAM-macOS-1.3.1.zip`
- Windows: `packages/YAM-Windows-1.3.1.zip`

`packages/YAM-<OS>-<version>/` の中には以下が入ります。

- `YAM.app` または `YAM.exe`
- `program-files/`
- `README.md`
- `LICENSE`

配布するときは、通常は `packages/` の zip をそのまま渡してください。`dist/` の中身だけを単体で渡す運用は推奨しません。

## ポートについて

- 既定ポートは `5000` です
- `5000` が使用中なら、自動で空いているローカルポートへ切り替えます
- 起動後は実際に使われた URL が表示され、ブラウザも自動で開きます

## 初期設定

1. YAM を起動する
2. `設定・統計` を開く
3. `YouTube API キー` を入力する
4. `チャンネルID / URL / @handle` に、同期したいチャンネルを入力する
5. `設定保存` を押す
6. `同期` を押す

## チャンネルの入力方法

チャンネルは複数指定できます。

入力できる形式:

- `UC...` で始まるチャンネル ID
- `https://www.youtube.com/@...`
- `https://www.youtube.com/channel/...`
- `@handle`

複数指定の例:

```text
https://www.youtube.com/@HakuiKoyori
https://www.youtube.com/@sakamatachloe
@laplus_darknesss
```

または:

```text
https://www.youtube.com/@HakuiKoyori, https://www.youtube.com/@sakamatachloe, @laplus_darknesss
```

改行区切りでもカンマ区切りでも構いません。

## YouTube API キーの取得方法

このツールは `YouTube Data API v3` の API キーを使います。

手順:

1. Google アカウントで Google Cloud Console / API Console を開く
2. 新しいプロジェクトを作るか、使うプロジェクトを選ぶ
3. `APIs & Services` → `Library` を開く
4. `YouTube Data API v3` を検索して `ENABLE` を押す
5. `APIs & Services` → `Credentials` を開く
6. `Create credentials` → `API key` を押す
7. 表示された API キーを YAM の設定へ貼り付ける

推奨:

- API キーは作成後に制限してください
- 少なくとも API restriction で `YouTube Data API v3` に絞るのを推奨します

参考:

- YouTube Data API Overview
  https://developers.google.com/youtube/v3/getting-started
- Manage API keys
  https://cloud.google.com/docs/authentication/api-keys
- Enable and disable APIs
  https://support.google.com/googleapi/answer/6158841

詳しくは `YouTube API キーの取得方法` や `YouTube Data API v3` で調べると、画像付きの解説も見つかります。

## 使い方

### 一覧

- 検索
- タグ絞り込み
- 視聴状態絞り込み
- 並び順切り替え
- 手動追加
- 個別編集
- 複数選択による一括操作

### 設定・統計

- API キー設定
- 複数チャンネル設定
- 言語切り替え
- 同期除外タグ設定
- アイコン変更
- バックアップ保持数設定
- 統計表示

## 検索の使い方

検索バーはスペース区切りで複数条件を入れられます。

### 基本

- `歌枠`
  `歌枠` を含む動画を検索

- `歌枠 コラボ`
  `歌枠` と `コラボ` の両方を含む動画を検索

### 除外検索

`-` を付けると除外できます。

- `歌枠 -切り抜き`
  `歌枠` を含み、`切り抜き` を含む動画を除外

- `3Dライブ -shorts -clip`
  `3Dライブ` を含み、`shorts` と `clip` を含むものを除外

### タグ候補

- 検索入力中にタグ候補が出ます
- 候補を押すとそのタグを検索条件へ追加できます
- `-タグ名` の形で除外条件にもできます

### タグプルダウン

- 右側のタグプルダウンは出現数の多い順です
- 複数選択できます
- ここで選んだタグは AND 条件で絞り込みます

## 手動追加

右上の `追加` から手動で動画を入れられます。

最低限必要な項目:

- URL
- 現在の視聴進捗 または 視聴済み

詳細を開くと設定できる項目:

- タイトル
- サムネ画像
- タグ
- 全体の長さ
- 感想 / メモ

## タグ編集

- 自動同期で入ったタグも、一覧の編集内のタグ欄でそのまま編集できます
- 複数選択で一括追加 / 一括削除もできます

## 統計

統計画面では次の確認ができます。

- 視聴進捗グラフ
- 指定条件に一致する動画の割合
- 条件付きの 1日平均 / 1か月平均配信時間

条件欄では通常検索と同じように除外検索が使えます。

例:

- `生配信 -shorts`
- `コラボ,歌枠 -切り抜き`

## データ保存先

- 設定: `data/config.json`
- 動画一覧: `data/videos.csv`
- 視聴進捗: `data/progress.csv`
- 視聴進捗履歴: `data/progress_history.csv`
- 感想 / メモ: `data/notes.csv`
- バックアップ: `data/backups/`
- アップロード画像: `data/uploads/`

## ライセンス

MIT License
詳細は [LICENSE](LICENSE) を参照してください。

## Credits

©IGNORANZ PROJECT

- [企画：じょしゅのうち](https://x.com/Josyuuchi_Joyu)
- [システム：江上 新](https://x.com/ArataEgami)
- [IGNORANZ PROJECT X](https://x.com/IGNORANZ_P)
- [IGNORANZ PROJECT 公式サイト](https://ignoranz-project.web.app/)
