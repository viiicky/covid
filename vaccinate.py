import asyncio
import json
from math import ceil
from time import sleep, perf_counter

import aiohttp as aiohttp
import requests
from datetime import datetime, date
from tabulate import tabulate
import os
from dotenv import load_dotenv

load_dotenv()


class Center:
    def __init__(self, center_id, name, sessions):
        self.center_id = center_id
        self.name = name
        self.sessions = sessions

    def __eq__(self, o: 'Center') -> bool:
        return self.center_id == o.center_id

    def __hash__(self) -> int:
        return hash(self.center_id)


async def send_telegram(chat_id, message, session):
    if message and chat_id:
        # print(f'channel: {chat_id}; centers:\n{message}')
        url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage?chat_id={chat_id}" \
              f"&parse_mode=HTML&text=<pre>{message}</pre>"
        async with session.post(url):
            pass


async def send_notifications(chat_ids, cova_18_message, cova_45_message, covi_18_message, covi_45_message):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            send_telegram(chat_ids.get('cova_18'), cova_18_message, session),
            send_telegram(chat_ids.get('cova_45'), cova_45_message, session),
            send_telegram(chat_ids.get('covi_18'), covi_18_message, session),
            send_telegram(chat_ids.get('covi_45'), covi_45_message, session)
        )


def get_calendar(district_id, search_date):
    response = requests.get(f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
                            f'?district_id={district_id}&date={search_date}', headers={'User-Agent': 'Mozilla/5.0 ('
                                                                                                     'Macintosh; '
                                                                                                     'Intel Mac OS X '
                                                                                                     '10_15_7) '
                                                                                                     'AppleWebKit/537'
                                                                                                     '.36 (KHTML, '
                                                                                                     'like Gecko) '
                                                                                                     'Chrome/90.0'
                                                                                                     '.4430.93 '
                                                                                                     'Safari/537.36'})
    response.raise_for_status()
    return response.json()


def get_hospitals(district_id, search_date):
    covaxin_18_hospitals = set()
    covaxin_45_hospitals = set()
    covishield_18_hospitals = set()
    covishield_45_hospitals = set()

    centers = get_calendar(district_id, search_date)['centers']
    for center in centers:
        for session in center['sessions']:
            if datetime.strptime(session['date'], '%d-%m-%Y').date() >= date.today() and session['available_capacity']:
                vaccine = session['vaccine'].strip().upper()
                new_center = Center(center['center_id'], center['name'], center['sessions'])
                if vaccine == 'COVAXIN':
                    if session['min_age_limit'] == 18:
                        covaxin_18_hospitals.add(new_center)
                    elif session['min_age_limit'] == 45:
                        covaxin_45_hospitals.add(new_center)
                elif vaccine == 'COVISHIELD':
                    if session['min_age_limit'] == 18:
                        covishield_18_hospitals.add(new_center)
                    elif session['min_age_limit'] == 45:
                        covishield_45_hospitals.add(new_center)

    return covaxin_18_hospitals, covaxin_45_hospitals, covishield_18_hospitals, covishield_45_hospitals


if __name__ == "__main__":
    districts = json.loads(os.environ['DISTRICTS'])
    while True:
        start = perf_counter()
        for district in districts:
            # find centers
            cova_18, cova_45, covi_18, covi_45 = get_hospitals(district['district_id'],
                                                               date.today().strftime('%d-%m-%Y'))


            def format_hospital(hospital):
                return {'name': hospital.name,
                        'available_capacity': [ceil(s['available_capacity']) for s in hospital.sessions]}


            # prepare output
            cova_18_output = tabulate([format_hospital(h) for h in cova_18])
            cova_45_output = tabulate([format_hospital(h) for h in cova_45])
            covi_18_output = tabulate([format_hospital(h) for h in covi_18])
            covi_45_output = tabulate([format_hospital(h) for h in covi_45])

            # send notifications
            asyncio.run(send_notifications(district, cova_18_output, cova_45_output, covi_18_output, covi_45_output))

        print(f'time taken: {perf_counter() - start} seconds')
        sleep(int(os.environ['SLEEP_SECONDS']))
