
MAX_USERS = 3  # максимальное кол-во пользователей
MAX_GPT_TOKENS = 150  # максимальное кол-во токенов в ответе GPT
COUNT_LAST_MSG = 4  # кол-во последних сообщений из диалога

# лимиты для пользователя
MAX_USER_STT_BLOCKS = 10  # 10 аудиоблоков
MAX_USER_TTS_SYMBOLS = 5_000  # 5 000 символов
MAX_USER_GPT_TOKENS = 2_000  # 2 000 токенов

SYSTEM_PROMPT = [{'role': 'system', 'text': 'Ты веселый собеседник. Общайся с пользователем на "ты" и используй юмор. '
                                            'Поддерживай диалог. Не объясняй пользователю, что ты умеешь и можешь. '

                                            'Изображай человека'}]

HEADERS_GPT = {
    'Authorization': f'Bearer   ',
    'Content-Type': 'application/json'
}
URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
HOME_DIR = '/home/student/finally'  # путь к папке с проектом
LOGS = 'logs.txt'  # файл для логов
DB_FILE = f'{HOME_DIR}/messages.db'  # файл для базы данных

IAM_TOKEN_PATH = f'{HOME_DIR}/creds/iam_token.txt'  # файл для хранения iam_token
FOLDER_ID_PATH = f'{HOME_DIR}/creds/folder_id.txt'  # файл для хранения folder_id
BOT_TOKEN_PATH = f'{HOME_DIR}/creds/token.txt'  # файл для хранения bot_token
