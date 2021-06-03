import asyncio
import json
from math import ceil
from time import sleep, perf_counter

import aiohttp as aiohttp
from datetime import datetime, date
from tabulate import tabulate
import os
from dotenv import load_dotenv
from fake_useragent import UserAgent

load_dotenv()
ua = UserAgent()


async def send_telegram(chat_id, message, session):
    if message and chat_id:
        # print(f'channel: {chat_id}; centers:\n{message}')
        url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage?chat_id={chat_id}" \
              f"&parse_mode=HTML&text=<pre>{message}</pre>"
        async with session.post(url) as resp:
            print(f'channel: {chat_id}; resp.status: {resp.status}; resp.text(): {await resp.text()}')


async def send_notifications(chat_ids, cova_18_message, cova_45_message, covi_18_message, covi_45_message, session):
    await asyncio.gather(
        send_telegram(chat_ids.get('cova_18'), cova_18_message, session),
        send_telegram(chat_ids.get('cova_45'), cova_45_message, session),
        send_telegram(chat_ids.get('covi_18'), covi_18_message, session),
        send_telegram(chat_ids.get('covi_45'), covi_45_message, session)
    )


async def get_calendar(district_id, search_date, session):
    url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={district_id}' \
          f'&date={search_date}'
    async with session.get(url, headers={'User-Agent': ua.random, 'Cache-Control': 'no-cache'}) as resp:
        return await resp.json()


async def get_hospitals(district_id, search_date, session):
    covaxin_18_hospitals = dict()
    covaxin_45_hospitals = dict()
    covishield_18_hospitals = dict()
    covishield_45_hospitals = dict()

    centers = (await get_calendar(district_id, search_date, session))['centers']
    for center in centers:
        for session in center['sessions']:
            if datetime.strptime(session['date'], '%d-%m-%Y').date() >= date.today() and session['available_capacity']:

                vaccine = session['vaccine'].strip().upper()
                center_id = center['center_id']
                new_center = {'name': center['name'], 'pincode': center['pincode'], 'sessions': []}

                if vaccine == 'COVAXIN':
                    if session['min_age_limit'] == 18:
                        if center_id not in covaxin_18_hospitals:
                            covaxin_18_hospitals[center_id] = new_center
                        covaxin_18_hospitals[center_id]['sessions'].append(session)
                    elif session['min_age_limit'] == 45:
                        if center_id not in covaxin_45_hospitals:
                            covaxin_45_hospitals[center_id] = new_center
                        covaxin_45_hospitals[center_id]['sessions'].append(session)
                elif vaccine == 'COVISHIELD':
                    if session['min_age_limit'] == 18:
                        if center_id not in covishield_18_hospitals:
                            covishield_18_hospitals[center_id] = new_center
                        covishield_18_hospitals[center_id]['sessions'].append(session)
                    elif session['min_age_limit'] == 45:
                        if center_id not in covishield_45_hospitals:
                            covishield_45_hospitals[center_id] = new_center
                        covishield_45_hospitals[center_id]['sessions'].append(session)

    return covaxin_18_hospitals, covaxin_45_hospitals, covishield_18_hospitals, covishield_45_hospitals


def format_hospital(hospital):
    return {'name': hospital['name'], 'pincode': hospital['pincode'],
            'sessions': [f"{s['date']}: {ceil(s['available_capacity_dose1'])}%2b{ceil(s['available_capacity_dose2'])}"
                         f"={ceil(s['available_capacity'])}" for s in hospital['sessions']]}


async def process_district(district, session):
    # find centers
    cova_18, cova_45, covi_18, covi_45 = await get_hospitals(district['district_id'], date.today().strftime('%d-%m-%Y'),
                                                             session)

    # prepare output
    cova_18_output = tabulate([format_hospital(h) for h in cova_18.values()])
    cova_45_output = tabulate([format_hospital(h) for h in cova_45.values()])
    covi_18_output = tabulate([format_hospital(h) for h in covi_18.values()])
    covi_45_output = tabulate([format_hospital(h) for h in covi_45.values()])

    # send notifications
    await send_notifications(district, cova_18_output, cova_45_output, covi_18_output, covi_45_output, session)


async def main():
    districts = json.loads(os.environ['DISTRICTS'])
    while True:
        start = perf_counter()
        async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(*(process_district(d, session) for d in districts), return_exceptions=True)
            for district, result in zip(districts, results):
                if isinstance(result, Exception):
                    error = f"exception occurred when district {district['district_id']} was being processed: {repr(result)}"
                    print(error)
                    try:
                        await send_telegram(os.environ['BOT_CHAT_ID'], error, session)
                    except Exception as e:
                        print(f'Sending error message to the bot itself errored out. Logging and swallowing the '
                              f'exception\n{e}')
        print(f'time taken: {perf_counter() - start} seconds')
        sleep(int(os.environ['SLEEP_SECONDS']))


if __name__ == '__main__':
    asyncio.run(main())
