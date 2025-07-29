import os
import datetime
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from pydub.silence import split_on_silence
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import openai

# 🔧 ffmpegのパス（pydub用）※自分の環境に合わせて変更してください
AudioSegment.converter = r"C:\path\to\ffmpeg.exe"

# 🔐 .envからトークン読込
load_dotenv(".env")
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🟢 Slackクライアント初期化
client = WebClient(token=SLACK_TOKEN)

# 🎙 録音設定
duration = 60 * 10  # 10分
fs = 44100
today = datetime.date.today()
raw_filename = f"sleep_record_{today}.wav"
trimmed_filename = f"sleep_record_trimmed_{today}.wav"

# ⏺ 録音
print("🔴 録音スタート...")
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()
sf.write(raw_filename, audio, fs)
print(f"✅ 録音完了: {raw_filename}")

# ✂️ 無音カット処理
print("🔎 無音カット中...")
sound = AudioSegment.from_wav(raw_filename)
silence_thresh = sound.dBFS - 14
chunks = split_on_silence(
    sound,
    min_silence_len=1000,
    silence_thresh=silence_thresh,
    keep_silence=300
)

if chunks:
    combined = AudioSegment.empty()
    for chunk in chunks:
        combined += chunk
    combined.export(trimmed_filename, format="wav")
    print(f"✅ 無音カット済みファイル保存: {trimmed_filename}")
    print(f"🟢 音声区間数: {len(chunks)}")
else:
    print("⚠️ 無音のみでカット対象なし")
    trimmed_filename = raw_filename
    combined = sound

# ☁️ Slackへ音声ファイル投稿
try:
    print("📤 Slackに送信中...")
    response = client.files_upload_v2(
        channel=SLACK_CHANNEL_ID,
        file=trimmed_filename,
        title=f"🎧 {trimmed_filename}",
        initial_comment="🎙 本日の睡眠音声ログ（無音カット済）"
    )
    print(f"✅ Slack投稿完了")
except SlackApiError as e:
    print(f"Slackエラー: {e.response['error']}")

# 💬 ChatGPTでコメント生成
try:
    print("🤖 GPTコメント生成中...")
    openai.api_key = OPENAI_API_KEY
    duration_sec = len(combined) / 1000
    prompt = f"""以下は睡眠中の音声記録です。音声の長さは {round(duration_sec, 1)} 秒でした。
この音声からわかることを簡単にコメントして下さい（環境音・発話・いびきなど）。"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    comment = response["choices"][0]["message"]["content"]
    print("📝 GPTコメント:")
    print(comment)

    client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=f"🧠 GPT分析コメント:\n{comment}")
except Exception as e:
    print(f"GPTエラー: {e}")
