TOKEN = "6781055175:AAGtdEuyR-iWe4ciSaMpmRm2fTktl4pia2I"  # token телеграм-бота

MAX_USERS = 3  # максимальное кол-во пользователей
MAX_GPT_TOKENS = 150  # максимальное кол-во токенов в ответе GPT
COUNT_LAST_MSG = 4  # кол-во последних сообщений из диалога

# лимиты для пользователя
MAX_USER_STT_BLOCKS = 10  # 10 аудиоблоков
MAX_USER_TTS_SYMBOLS = 5_000  # 5 000 символов
MAX_USER_GPT_TOKENS = 2_000  # 2 000 токенов

LOGS = 'logs.txt'  # файл для логов
DB_FILE = 'messages.db'  # файл для базы данных
SYSTEM_PROMPT = [{'role': 'system', 'text': 'Ты веселый собеседник. Общайся с пользователем на "ты" и используй юмор. '
                                            'Поддерживай диалог. Не объясняй пользователю, что ты умеешь и можешь. '
     
                                            'Изображай человека'}]
IAM_TOKEN = 't1.9euelZqWls6VnsqPnZSQlpSNl82Xj-3rnpWaisaTlpDNm8yTjYmYlpiayMvl8_dpWwFO-e8_EngY_t3z9ykKf0357z8SeBj-zef1656VmpbHkJqcxpGJlo3Lk5LNnozL7_zF656VmpbHkJqcxpGJlo3Lk5LNnozLveuelZrLnMrLyJOeyZCNl5WVlo-Nk7XehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.8peSeK-w_ylPJgn5jdM4t0UTNQe2qbNVDL-Eu7AdyD7L8qG1YmRAyhM9W073ZbjC1rXo5A9XLojVf8zEmkM7Dw'

FOLDER_ID= 'b1ghfb4epm2t95ql7k0d'