import requests
import concurrent.futures
from fimparser import parse_chair_page, parse_chair_landingpage, parse_chair_team

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

def get_chair_data():
    chair_data = []
    chair_page = requests.get(CHAIR_OVERVIEW_URL).text
    chair_links = parse_chair_page(chair_page)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_link = {executor.submit(parse_chair, link): link for link in chair_links}
        for future in concurrent.futures.as_completed(future_to_link):
            link = future_to_link[future]
            try:
                chair = future.result()
                chair_data.append(chair)
            except Exception as e:
                print(f'Failed to parse chair: {link}: {e}')

    return chair_data

def parse_chair(link):
    print(f'Parsing chair: {link}')

    chair_req = requests.get(link)
    if chair_req.status_code != 200:
        raise Exception(f'request was not successful: {chair_req.status_code}')

    chair_name, chair_team_link = parse_chair_landingpage(chair_req.text)

    chair_team_page = requests.get(chair_team_link).text
    chair_team = parse_chair_team(chair_team_page)

    chair = UniversityChair(chair_name)
    for member in chair_team:
        chair.add_team_member(member)

    return chair

