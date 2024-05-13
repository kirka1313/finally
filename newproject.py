import telebot
from newvalidators import *
from newconfig import COUNT_LAST_MSG, LOGS
from mewdatabase import create_database, add_message, select_n_last_messages
from newcount import speech_to_text, text_to_speech, ask_gpt
from creds import get_bot_token

bot = telebot.TeleBot(get_bot_token())
logging.basicConfig(filename=LOGS, level=logging.INFO,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Привет! Отправь мне голосовое сообщение или текст, и я тебе отвечу!")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, "Чтобы приступить к общению, отправь мне голосовое сообщение или текст")


@bot.message_handler(commands=['debug'])
def debug(message):
    with open("logs.txt", "rb") as f:
        bot.send_document(message.chat.id, f)


@bot.message_handler(content_types=['voice'])
def handle_voice(message: telebot.types.Message):
    user_id = message.from_user.id
    status_check_users, error_message = check_number_of_users(user_id)
    if not status_check_users:
        bot.send_message(user_id, error_message)
        return

    stt_blocks, error_message = is_stt_block_limit(user_id, message.voice.duration)
    if error_message:
        bot.send_message(user_id, error_message)
        return

    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)
    status_stt, stt_text = speech_to_text(file)
    if not status_stt:
        bot.send_message(user_id, stt_text)
        return

    add_message(user_id=user_id, full_message=[stt_text, 'user', 0, 0, stt_blocks])
    last_messages, total_spent_tokens = select_n_last_messages(user_id, COUNT_LAST_MSG)
    total_gpt_tokens, error_message = is_gpt_token_limit(last_messages, total_spent_tokens)
    if error_message:
        bot.send_message(user_id, error_message)
        return

    status_gpt, answer_gpt, tokens_in_answer = ask_gpt(last_messages)
    if not status_gpt:
        bot.send_message(user_id, answer_gpt)
        return

    total_gpt_tokens += tokens_in_answer
    tts_symbols, error_message = is_tts_symbol_limit(user_id, answer_gpt)
    add_message(user_id=user_id, full_message=[answer_gpt, 'assistant', total_gpt_tokens, tts_symbols, 0])
    if error_message:
        bot.send_message(user_id, f"вы превысили лимит токенов,даю вам последний ответ в текстовом виде {answer_gpt}")
        return

    status_tts, voice_response = text_to_speech(answer_gpt)
    if status_tts:
        bot.send_voice(user_id, voice_response, reply_to_message_id=message.id)
    else:
        bot.send_message(user_id, answer_gpt, reply_to_message_id=message.id)


@bot.message_handler(commands=['stt', 'tts'])
def speech_text(message):
    bot.send_message(message.chat.id, 'Отправьте голосовое сообщение и я переведу в иной вид')
    bot.register_next_step_handler(message, speech_to_text_or_rather)


def speech_to_text_or_rather(message):
    if message.content_type == 'voice':
        stt_blocks = is_stt_block_limit(message, message.voice.duration)
        if not stt_blocks:
            bot.send_message(message.chat.id, 'чет у вас не так')
            return
        file_info = bot.get_file(message.voice.file_id)
        file = bot.download_file(file_info.file_path)
        status, text = speech_to_text(file)
        if not status:
            bot.send_message(message.chat.id, f'Произошла ошибка {text}')
            return
        bot.send_message(message.chat.id, text)
        return
    elif message.content_type == 'text':
        text_symbols = len(message.text)
        if text_symbols > 100:
            bot.send_message(message.chat.id, 'ну не наглей,сто символов будет достаточно тебе')
            return
        tts_symbols, error = is_tts_symbol_limit(message.chat.id, message.text)
        if error:
            bot.send_message(message.chat.id, 'закончились токены')
            return
        status, content = text_to_speech(message.text)
        if not status:
            bot.send_message(message.chat.id, content)
            return
        with open("output.ogg", "wb") as audio_file:
            audio_file.write(content)
        bot.send_voice(message.chat.id, content)



@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    status_check_users, error_message = check_number_of_users(user_id)
    if not status_check_users:
        bot.send_message(user_id, error_message)  # мест нет =(
        return

    full_user_message = [message.text, 'user', 0, 0, 0]
    add_message(user_id=user_id, full_message=full_user_message)
    last_messages, total_spent_tokens = select_n_last_messages(user_id, COUNT_LAST_MSG)
    total_gpt_tokens, error_message = is_gpt_token_limit(last_messages, total_spent_tokens)
    if error_message:
        bot.send_message(user_id, error_message)
        return

    status_gpt, answer_gpt, tokens_in_answer = ask_gpt(last_messages)
    if not status_gpt:
        bot.send_message(user_id, answer_gpt)
        return
    total_gpt_tokens += tokens_in_answer

    full_gpt_message = [answer_gpt, 'assistant', total_gpt_tokens, 0, 0]
    add_message(user_id=user_id, full_message=full_gpt_message)
    bot.send_message(user_id, answer_gpt, reply_to_message_id=message.id)


create_database()
bot.polling()
