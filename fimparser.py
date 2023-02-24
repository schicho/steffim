from bs4 import BeautifulSoup

FIM_URL_PREFIX = 'https://www.fim.uni-passau.de'


def _convert_to_full_url(url):
    if not url.startswith('http'):
        return FIM_URL_PREFIX + url
    return url


'''
This function parses the chair overview page.
It finds the links to the chairs and their names as tuples.
'''


def parse_chair_page(chair_page):
    soup = BeautifulSoup(chair_page, 'html.parser')

    # tuples of (link, name)
    chairWithLink = []

    # the links to the chairs are in a table
    # unfortunately, the table does not have a disctinctive class or id
    # however, the table is inside the <main> tag and each chair can be found in a <tr> and <td> tag

    trTags = soup.find('main').find_all('tr')
    for trTag in trTags:
        # the link to the chair is in the second <td> tag
        # see chairs.html line 1250...
        tdTags = trTag.find_all('td')
        if len(tdTags) > 1:
            aLink = tdTags[1].find('a')
            chairName = aLink.text
            linkToChair = aLink.get('href')

            # the link may be relative, so we need to add the prefix
            linkToChair = _convert_to_full_url(linkToChair)

            chairWithLink.append((linkToChair, chairName))

    return chairWithLink


'''
This function parses the landing page of a chair.
It finds the link to the chair's team page.
'''


def parse_chair_landingpage(chair_landingpage):
    soup = BeautifulSoup(chair_landingpage, 'html.parser')

    # find the link to the chair's team page
    # the link can be found by looking for the first occurence of the text "team"
    # as the links can have different style, e.g. "Lehrstuhlteam" or "Team"
    # yes, this is an extreme hack, but it works

    linkToTeam = None
    for link in soup.find_all('a'):
        if link.text.lower().find('team') != -1:
            linkToTeam = link.get('href')
            break

    if linkToTeam is None:
        raise Exception('Failed to find link to team page')

    return _convert_to_full_url(linkToTeam)


'''
This function parses the chair team page.
It finds the names of the chair team members.
'''


def parse_chair_team(chair_team_page):
    soup = BeautifulSoup(chair_team_page, 'html.parser')

    memberNames = []

    # the chair team members are in multiple tables
    # the tables cannot be simply found by their class or id
    # as such, we find the all tables in the <main> tag and look at all the links in the tables
    #
    # the links are the chair team members and their email addresses
    # we are only interested in the links that do not start with "mailto:"
    #
    # from the <a> we can get the names of the chair team members

    for table in soup.find('main').find_all('table'):
        for link in table.find_all('a'):
            if link.get('href').find('mailto:') == -1:
                memberNames.append(link.text)

    return memberNames
