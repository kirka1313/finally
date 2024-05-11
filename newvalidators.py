import logging
from mewdatabase import count_users, count_all_limits
import requests
from newconfig import *
from creds import get_creds
logging.basicConfig(filename=LOGS, level=logging.ERROR, format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")

IAM_TOKEN, FOLDER_ID = get_creds()

def count_gpt_tokens(messages):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion"
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "messages": messages
    }
    try:
        return len(requests.post(url=url, json=data, headers=headers).json()['tokens'])
    except Exception as e:
        logging.info(e)
        return 0


def check_number_of_users(user_id):
    count = count_users(user_id)
    if count is None:
        return None, "Ошибка при работе с БД"
    if count > MAX_USERS:
        return None, "Превышено максимальное количество пользователей"
    return True, ""


def is_gpt_token_limit(messages, total_spent_tokens):
    all_tokens = count_gpt_tokens(messages) + total_spent_tokens
    if all_tokens > MAX_USER_GPT_TOKENS:
        return None, f"Превышен общий лимит GPT-токенов {MAX_USER_GPT_TOKENS}"
    return all_tokens, ""


def is_stt_block_limit(user_id, duration):
    if duration > 30:
        return None, 'слишкамтлахуя длина'
    blocks = count_all_limits(user_id, 'stt_blocks')
    if blocks > MAX_USER_STT_BLOCKS:
        return None, 'idi nah'
    return blocks, ''


def is_tts_symbol_limit(user_id, text):
    symbols = count_all_limits(user_id, 'tts_symbols')
    if symbols > MAX_USER_TTS_SYMBOLS:
        return None, 'idi nah'
    return symbols, ''