import requests
import json
from datetime import datetime
import logging
from fimparser import parse_chair_overview, parse_individual_chair_landing, parse_individual_chair_team
import aiohttp, asyncio

CHAIR_OVERVIEW_URL = 'https://www.fim.uni-passau.de/forschung-und-professuren/lehrstuehle-professuren-und-fachgebiete'


class UniversityChair:
    def __init__(self, name):
        self.name = name
        self._team = []
        self._stef = []

    def add_team_member(self, member: str):
        self._team.append(member)

        if member.lower().find('stef') > -1 or member.lower().find('steph') > -1:
            self._stef.append(member)

    def __str__(self):
        return f'{self.name} has {len(self._team)} team members, ' \
            f'including {len(self._stef)} Stef(s): {self._stef}'

    def __repr__(self):
        return self.__str__()

    def stef_stats(self):
        return (self.name, len(self._stef))

    def stef_list(self):
        return self._stef.copy()


async def get_chair_data():
    logging.debug('getting chair overview page')

    async with aiohttp.ClientSession() as session:
        resp = await session.get(CHAIR_OVERVIEW_URL)
        if resp.status != 200:
            raise Exception(f'request to overview page was not successful: {resp.status}')

        chair_page_text = await resp.text()
        chair_info = parse_chair_overview(chair_page_text)

        chair_data = []
        tasks = [get_individual_chair(session, chair_link_tuple) for chair_link_tuple in chair_info]
        for future in asyncio.as_completed(tasks):
            try:
                chair = await future
                chair_data.append(chair)
            except Exception as e:
                logging.warning(f'failed to parse chair: {e}')

    return chair_data

async def get_individual_chair(session, chair_link_tuple):
    logging.debug(f'getting chair: {chair_link_tuple[0]}')

    resp = await session.get(chair_link_tuple[1])
    if resp.status != 200:
        raise Exception(f'request for chair {chair_link_tuple[1]} was not successful: {resp.status}. link: {chair_link_tuple[1]}')

    chair_team_link = parse_individual_chair_landing(chair_link_tuple, await resp.text())

    resp = await session.get(chair_team_link)
    if resp.status != 200:
        raise Exception(f'request for teampage of chair {chair_link_tuple[0]} was not successful: {resp.status}. link: {chair_team_link}')
    
    # add context of chair to exception
    try:
        chair_team = parse_individual_chair_team(await resp.text())
    except Exception as e:
        raise Exception(f'{e} for chair {chair_link_tuple[0]}')

    chair = UniversityChair(chair_link_tuple[0])
    for member in chair_team:
        chair.add_team_member(member)

    return chair

def chair_data_to_json(chair_data):
    data = [{'chair_name': chair.name, 'stef_list': chair._stef} for chair in chair_data]

    json_data = f'{{"timestamp": "{datetime.now().timestamp()}", "data": {json.dumps(data, indent=2)}}}'
    return json_data
