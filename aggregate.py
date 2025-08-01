import asyncio
import json
import logging
from datetime import datetime

import aiohttp

from fimparser import parse_chair_overview, ChairParser

CHAIR_OVERVIEW_URL = "https://www.fim.uni-passau.de/forschung-und-professuren/lehrstuehle-professuren-und-fachgebiete"


class UniversityChair:
    def __init__(self, name):
        self.name = name
        self._team = []
        self._stef = []

    def add_team_member(self, member: str):
        self._team.append(member)

        if member.lower().find("stef") > -1 or member.lower().find("steph") > -1:
            self._stef.append(member)

    def __str__(self):
        return (
            f"{self.name} has {len(self._team)} team members, "
            f"including {len(self._stef)} Stef(s): {self._stef}"
        )

    def __repr__(self):
        return self.__str__()

    def stef_stats(self):
        return (self.name, len(self._stef))

    def stef_list(self):
        return self._stef.copy()


async def get_chair_data():
    logging.debug("getting chair overview page")

    async with aiohttp.ClientSession() as session:
        resp = await session.get(CHAIR_OVERVIEW_URL)
        if resp.status != 200:
            raise Exception(
                f"request to overview page was not successful: {resp.status}"
            )

        chair_page_text = await resp.text()
        chair_info = parse_chair_overview(chair_page_text)

        chair_data = []
        tasks = [
            get_individual_chair(session, chair_link_tuple)
            for chair_link_tuple in chair_info
        ]
        for future in asyncio.as_completed(tasks):
            try:
                chair = await future
                chair_data.append(chair)
            except Exception as e:
                logging.error(f"{e}. Failed to get data for chair")

    return chair_data


async def get_individual_chair(session, chair_link_tuple):
    logging.debug(f"getting chair: {chair_link_tuple[0]}")

    resp = await session.get(chair_link_tuple[1])
    if resp.status != 200:
        raise Exception(
            f"{chair_link_tuple[0]}: request to chair was not successful. response code: {resp.status}. link: {chair_link_tuple[1]}"
        )

    chair_parser = ChairParser(chair_link_tuple[0])

    chair_team_link = chair_parser.parse_landing_page(
        chair_link_tuple[1], await resp.text()
    )

    resp = await session.get(chair_team_link)
    if resp.status != 200:
        raise Exception(
            f"{chair_link_tuple[0]} request to team page was not successful. response code: {resp.status}. link: {chair_team_link}"
        )

    # add context of chair to exception
    try:
        chair_team = chair_parser.parse_team_page(await resp.text())
    except Exception as e:
        raise Exception(f"{chair_link_tuple[0]}: {e}")

    chair = UniversityChair(chair_link_tuple[0])
    for member in chair_team:
        chair.add_team_member(member)

    return chair


def chair_data_to_json(chair_data):
    data = [
        {"chair_name": chair.name, "stef_list": chair._stef} for chair in chair_data
    ]
    data.sort(key=lambda chair: chair["chair_name"])

    json_data = json.dumps({"timestamp": str(datetime.now().timestamp()), "data": data}, indent=2)
    return json_data
