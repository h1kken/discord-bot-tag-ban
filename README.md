# Discord Tag Ban

<p align="center">
  <strong>Русский</strong> · <a href="./READMEs/README_EN.md">English</a>
</p>

## Описание

Бот проверяет участников:

- при входе на сервер
- при отправке сообщения

Если найден запрещённый тег, бот:

- удаляет сообщение
- кикает с сервера

## Установка

1. Установи зависимости:

```bash
pip install -r requirements.txt
```

2. Создай `.env`:

```env
BOT_TOKEN=your_discord_bot_token
```

3. Укажи запрещённые ID тегов в [`main.py`](./main.py):

```python
BLOCKED_TAG_IDS = {
    123456789012345678,
}
```

4. Запусти бота:

```bash
python main.py
```