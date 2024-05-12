import logging
from newconfig import MAX_GPT_TOKENS, SYSTEM_PROMPT, URL, HEADERS_GPT
import requests
from newvalidators import count_gpt_tokens
from creds import get_creds

IAM_TOKEN, FOLDER_ID = get_creds()


def ask_gpt(messages):
    url = URL
    headers = HEADERS_GPT
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": MAX_GPT_TOKENS
        },
        "messages": SYSTEM_PROMPT + messages  # добавляем к системному сообщению предыдущие сообщения
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            return False, f"Ошибка GPT. Статус-код: {response.status_code}", None
        answer = response.json()['result']['alternatives'][0]['message']['text']
        tokens_in_answer = count_gpt_tokens([{'role': 'assistant', 'text': answer}])
        return True, answer, tokens_in_answer
    except Exception as e:
        logging.error(e)
        return False, "Ошибка при обращении к GPT", None


def speech_to_text(data):
    params = "&".join([
        "topic=general",
        f"folderId={FOLDER_ID}",
        "lang=ru-RU"
    ])
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
    }
    response = requests.post(
        f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}",
        headers=headers,
        data=data
    )

    decoded_data = response.json()
    if decoded_data.get("error_code") is None:
        return True, decoded_data.get("result")
    else:
        logging.error('ошибка при преобразовании войса в текст')
        return False, "При запросе в SpeechKit возникла ошибка"


def text_to_speech(text: str):
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
    }
    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': 'filipp',
        'folderId': FOLDER_ID,
    }

    response = requests.post('https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize', headers=headers,
                             data=data)

    if response.status_code == 200:
        return True, response.content
    else:
        logging.error('ошибка при преобразовании text в voice')
        return False, "При запросе в SpeechKit возникла ошибка"
