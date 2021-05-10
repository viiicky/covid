from time import sleep, perf_counter
import requests
from datetime import datetime, date
from tabulate import tabulate
from telethon.sync import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://cdn-api.co-vin.in'

telegram_client = TelegramClient(os.environ.get('TELEGRAM_SESSION_NAME'), os.environ.get('TELEGRAM_API_ID'), os.environ.get('TELEGRAM_API_HASH'))


def send_telegram(body, to):
    with telegram_client:
        entity = telegram_client.get_entity(to)
        telegram_client.send_message(entity=entity, message=body)


def get_calendar(district, search_date):
    headers = {
        'Accept-Language': 'en_US',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.85 Safari/537.36 '
    }

    query_url = f'{BASE_URL}/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district}&date={search_date}'

    response = requests.get(query_url, headers=headers)
    response.raise_for_status()

    return response.json()


def get_hospitals(district, search_date):
    hospitals = []
    centers = get_calendar(district, search_date)['centers']
    for center in centers:
        for session in center['sessions']:
            if datetime.strptime(session['date'], '%d-%m-%Y').date() >= date.today() and session['min_age_limit'] == 18 and session['available_capacity'] > 0 and session['vaccine'] == 'COVAXIN':
                hospitals.append(center)
                break

    return hospitals


def send_notifications(message):
    send_telegram(message, os.environ.get('TELEGRAM_HOME_GROUP_INVITE_LINK'))


if __name__ == "__main__":
    while True:
        start = perf_counter()
        h = get_hospitals(os.environ.get('DISTRICT_ID'), date.today().strftime('%d-%m-%Y'))
        for hospital in h:
            hospital.pop('center_id')
            hospital.pop('state_name')
            hospital.pop('district_name')

            for sess in hospital['sessions']:
                sess.pop('session_id')
                sess.pop('min_age_limit')

        output = tabulate(h, headers='keys', showindex='always')
        trimmed_output = tabulate([{'name': x['name'], 'address': x['address'], 'available_capacity':[y['available_capacity'] for y in x['sessions']]} for x in h])
        print(output)
        if trimmed_output:
            # print(trimmed_output)
            send_notifications(trimmed_output)
        print(f'time taken: {perf_counter() - start} seconds')

        sleep(3)
