# Discord Tag Ban

<p align="center">
  <a href="../README.md">Русский</a> · <strong>English</strong>
</p>

## Overview

This bot checks members for blocked guild tags:

- on member join
- on message send

If a blocked tag is found, the bot:

- deletes the triggering message if needed
- kicks from the server

## Install

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create `.env`:

```env
BOT_TOKEN=your_discord_bot_token
```

3. Set your blocked tag IDs in [`main.py`](./main.py):

```python
BLOCKED_TAG_IDS = {
    123456789012345678,
}
```

4. Run the bot:

```bash
python main.py
```