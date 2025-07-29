# Sleep Logger with Silence Cut and Slack Report

This project records a 10-minute sleep audio log, removes silent segments, uploads the result to Slack, and generates a summary using ChatGPT.

## Requirements

- ffmpeg (set the path in `sleep_logger.py`)
- Python packages:
  - sounddevice
  - soundfile
  - pydub
  - slack_sdk
  - openai
  - python-dotenv

## Setup

1. Copy `.env.example` to `.env` and add your tokens.
2. Adjust the path to ffmpeg in `sleep_logger.py`.
3. Run `record_sleep.bat` or schedule it with Windows Task Scheduler.

## License

MIT
