import os
import sys
import time
import logging

import requests
import telegram
from http import HTTPStatus
from dotenv import load_dotenv

from exception import WrongResponseCode


load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверка переменных окружения."""
    environmet_variables = (
        'PRACTICUM_TOKEN',
        'TELEGRAM_TOKEN',
        'TELEGRAM_CHAT_ID'
    )
    for token in environmet_variables:
        if token in globals():
            return all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))
        else:
            return f'Отсутсвтует токен {token}'


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except telegram.error.TelegramError as error:
        logging.error(f'Ошибка отправки статуса: {error}')
    else:
        logging.debug('Статус отправлен!')


def get_api_answer(timestamp):
    """Делаем запрос у API Практикум Домашки."""
    payload = {'from_date': timestamp}
    try:
        response = requests.get(url=ENDPOINT, headers=HEADERS, params=payload)
        if response.status_code != HTTPStatus.OK:
            raise WrongResponseCode(
                'Ошибка в ответе API'
                f'Код ответа: {response.status_code}'
                f'Причина: {response.reason}')
        return response.json()
    except requests.exceptions.RequestException:
        raise WrongResponseCode('Сбой при запросе к эндпоинту API')


def check_response(response):
    """Проверка  ответа API на соотвествие документации."""
    if not isinstance(response, dict):
        raise TypeError('Ответ API - не словарь')
    if 'homeworks' not in response:
        raise KeyError('Нет ключа "homeworks" в ответе')
    homeworks = response.get('homeworks')
    current_date = response.get('current_date')
    if not isinstance(homeworks, list):
        raise TypeError('homeworks не является списком')
    if not isinstance(current_date, int):
        raise TypeError('current_date не является целым числом')
    return homeworks


def parse_status(homework):
    """Извлекает из информации о конкретной домашней работе статус работы."""
    if 'homework_name' not in homework:
        raise KeyError('Нет нужного ключа в ответе')
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_status not in HOMEWORK_VERDICTS:
        raise ValueError(f'Неизвестный статус работы - {homework_status}')
    return ('Изменился статус проверки работы "{homework_name}". {verdict}'
            ).format(homework_name=homework_name,
                     verdict=HOMEWORK_VERDICTS[homework_status])


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        message = check_tokens()
        logging.critical(message)
        sys.exit(message)

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())

    while True:
        try:
            homeworks = get_api_answer(timestamp)
            homeworks_list = homeworks.get('homeworks')
            if check_response(homeworks):
                timestamp = homeworks.get('current_date')
                for homework in homeworks_list:
                    message = parse_status(homework)
                    send_message(bot, message)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            send_message(bot, message)

        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s, %(name)s, %(levelname)s'
        '%(message)s, %(funcName)s, %(lineno)d',
        handlers=[logging.StreamHandler(sys.stdout)],
        level=logging.ERROR)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    main()
