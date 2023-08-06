# neuro-bot

Бот поможет облегчить общение при помощи обработки натурального языка с помощью DialogFlow.

### Как установить

Python должен быть установлен.
Для запуска необходимо установить библиотеки с помощью `pip`:
```
pip install -r requirements.txt
```

## Переменные окружения

Настройки бота берутся из переменных окружения. Чтобы их определить, создайте файл `.env` в папке скрипта и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

**Для запуска проекта требуются три переменные**:
- `PROJECT_ID` — ID проекта гугла, в котором используется DialogFlow.
- `TG_TOKEN` — токен телеграм бота.
- `VK_TOKEN` — токен API вконтакте.
- `GOOGLE_APPLICATION_CREDENTIALS` - путь к .json файлу с ключами от вашего Google-аккаунта

### Как запустить 
Настройка бота производится при помощи консоли [DialogFlow](https://dialogflow.cloud.google.com)
Чтобы бот начал работу необходимо запустить файл `dialogflow_bot_for_vk.py` либо `dialogflow_bot_for_tg.py`

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).