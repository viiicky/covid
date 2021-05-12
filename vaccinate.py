from time import sleep, perf_counter
import requests
from datetime import datetime, date
from tabulate import tabulate
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://cdn-api.co-vin.in'


def send_telegram(message):
    send_text_url = f"https://api.telegram.org/bot{os.environ.get('TELEGRAM_BOT_TOKEN')}/sendMessage" \
                    f"?chat_id={os.environ.get('TELEGRAM_BOT_CHAT_ID')}&parse_mode=HTML&text=<pre>{message}</pre>"
    requests.get(send_text_url)


def send_notifications(message):
    send_telegram(message)


def get_calendar(district, search_date):
    response = requests.get(
        f'{BASE_URL}/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district}&date={search_date}',
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/90.0.4430.93 Safari/537.36'})

    response.raise_for_status()
    return response.json()


def get_hospitals(district, search_date):
    hospitals = []
    centers = get_calendar(district, search_date)['centers']
    print(f"all centers:\n{tabulate(centers, headers='keys', showindex='always')}")
    for center in centers:
        for session in center['sessions']:
            if datetime.strptime(session['date'], '%d-%m-%Y').date() >= date.today() \
                    and session['min_age_limit'] == 18 \
                    and session['available_capacity'] > 0 \
                    and session['vaccine'] == 'COVAXIN':
                hospitals.append(center)
                break

    return hospitals


if __name__ == "__main__":
    try:
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
            trimmed_output = tabulate([{'name': x['name'], 'address': x['address'],
                                        'available_capacity': [y['available_capacity'] for y in x['sessions']]} for x in
                                       h])
            print(f"filtered centers:\n{output}")
            if trimmed_output:
                # print(f"filtered centers:\n{trimmed_output}")
                send_notifications(trimmed_output)
            print(f'time taken: {perf_counter() - start} seconds')

            sleep(int(os.environ.get('SLEEP_SECONDS')))
    except Exception as e:
        print(e)
        send_notifications(e)
