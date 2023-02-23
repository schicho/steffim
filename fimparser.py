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
