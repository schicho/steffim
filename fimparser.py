from bs4 import BeautifulSoup

def parse_chair_page(chair_page):
    soup = BeautifulSoup(chair_page, 'html.parser')
    
    linksToChairs = []

    # the links to the chairs are in a table
    # unfortunately, the table does not have a disctinctive class or id
    # however, the table is inside the <main> tag and each chair can be found in a <tr> and <td> tag

    trTags = soup.find('main').find_all('tr')
    for trTag in trTags:
        # the link to the chair is in the second <td> tag
        # see chairs.html line 1250...
        tdTags = trTag.find_all('td')
        if len(tdTags) > 1:
            linkToChair = tdTags[1].find('a').get('href')
            linksToChairs.append(linkToChair)

    return linksToChairs

'''
This function parses the landing page of a chair.
It finds the name of the chair and the link to the chair's team page.

The parsing is absolutely hacky, but it works (currently).
The name is found in the first <h1> tag of the page.

The link to the chair's team page is found by looking for the first occurence of the text "team" in a link.
This must be done this way as each chair has a different link to their team page. e.g. "Lehrstuhlteam" or "Team".
'''
def parse_chair_landingpage(chair_landingpage):
    soup = BeautifulSoup(chair_landingpage, 'html.parser')
    
    # the chair name is in the <h1> tag
    chairName = soup.find('h1').text

    # find the link to the chair's team page
    # the link can be found by looking for the first occurence of the text "team"
    # yes, this is an extreme hack, but it works

    linkToTeam = None
    for link in soup.find_all('a'):
        if link.text.lower().find('team') != -1:
            linkToTeam = link.get('href')
            break

    return chairName, linkToTeam