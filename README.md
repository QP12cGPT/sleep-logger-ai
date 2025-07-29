# 💤 Sleep Logger AI：いびき検知＆GPT分析システム

このプロジェクトは、睡眠中の音声を10分間録音し、
- 無音を自動でカット
- Slackに録音ファイルを自動アップロード
- ChatGPTが音声内容を分析してコメント

までを自動で行うPythonスクリプトです。

---

## 📦 機能一覧
- 🎙️ 10分間の睡眠録音（`.wav`）
- ✂️ 無音区間の自動削除（`pydub.silence`）
- ☁️ Slackに録音ファイルを投稿
- 🤖 ChatGPT（gpt-3.5-turbo）によるコメント生成

---

## 🧰 必要ライブラリ

```bash
pip install sounddevice soundfile pydub slack_sdk python-dotenv openai
````

また、`ffmpeg` がローカルに必要です。以下から入手できます：

[https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)

---

## 🔐 .envファイル（例）

`.env` というファイルを作成し、以下のように記述します：

```env
SLACK_BOT_TOKEN=your-slack-bot-token
SLACK_CHANNEL_ID=your-channel-id
OPENAI_API_KEY=your-openai-api-key
```

`.env.example` も参考にしてください。

---

## ▶️ 実行方法

手動で実行する場合：

```bash
python sleep_logger.py
```

または、`record_sleep.bat` を実行。

---

## ⏰ 自動化（タスクスケジューラ）

1. `record_sleep.bat` を右クリック → タスクスケジューラに登録
2. 任意の時刻・頻度で自動実行可能
3. Slackに自動で音声＆GPTコメントが届きます！

---

## 🧠 GPT分析コメント（例）

```
この音声記録からは、深い睡眠中であることが伺えます。いびきや呼吸音が安定しており、リラックスした状態で眠っている様子です。
```

---

## 🗂️ ファイル構成

| ファイル           | 説明                              |
| ----------------- | ----------------------------------|
| sleep\_logger.py  | メイン処理スクリプト                |
| record\_sleep.bat | Windows自動化用バッチファイル       |
| .env.example      | 環境変数テンプレート                |
| .gitignore        | APIキーなどをGitに含めないための設定 |

---

## 🌐 English Summary

This project records 10 minutes of sleep audio, cuts silence, uploads to Slack, and generates a summary comment using ChatGPT. See `sleep_logger.py` for the main script.

---

## 🤝 免責事項

このコードは個人利用を目的としており、医療診断を目的としたものではありません。

---

## 📬 Contact

ご質問・改善案は [Issues](https://github.com/QP12cGPT/sleep-logger-ai/issues) または note にてお気軽に！
