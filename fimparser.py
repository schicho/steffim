import logging

from bs4 import BeautifulSoup

FIM_URL_PREFIX = "https://www.fim.uni-passau.de"


def _convert_to_full_url(path_or_url):
    if not path_or_url.startswith("http"):
        return FIM_URL_PREFIX + path_or_url
    return path_or_url


"""
This function creates a full url for the team page of a chair.
The logic is a bit complicated, because a chair page may be hosted on the FIM server and the path_or_url is relative.
Or the chair page is hosted on a different server and the path_or_url is relative as well.
Or the path_or_url is already a full url.
"""


def _convert_to_full_team_url(path_or_url, link_to_chair):
    # The chair page is hosted on the FIM site and the path_or_url to the team page is relative.
    # So we need to concatenate with the FIM_URL_PREFIX.
    if link_to_chair.startswith(FIM_URL_PREFIX):
        return FIM_URL_PREFIX + path_or_url

    # a full url is already used in the html
    if path_or_url.startswith("http"):
        return path_or_url

    # the path_or_url is relative, but the chair page is not hosted on the FIM server
    # so we need to concatenate with the link_to_chair
    if not path_or_url.startswith("http"):
        return link_to_chair + path_or_url
    return path_or_url


"""
This function parses the chair overview page.
It finds the links to the chairs and their names as tuples.
"""


def parse_chair_overview(chair_page):
    logging.debug("parsing chair overview page")
    soup = BeautifulSoup(chair_page, "html.parser")

    # tuples of (name, link)
    chair_link_touple_list = []

    # the links to the chairs are in a table
    # unfortunately, the table does not have a disctinctive class or id
    # however, the table is inside the <main> tag and each chair can be found in a <tr> and <td> tag

    table = soup.find("main").find("table")
    if table is None:
        raise Exception("no table of chairs found in the overview page")

    trTags = soup.find("main").find_all("tr")
    for trTag in trTags:
        # the link to the chair is in the second <td> tag
        # see chairs.html line 1250...
        tdTags = trTag.find_all("td")
        if len(tdTags) > 1:
            aLink = tdTags[1].find("a")

            if aLink is None:
                # the chair has no dedicated page, so we skip it
                logging.warning(
                    f"failed to find link: chair {tdTags[1].text} is listed, but has no dedicated page"
                )
                continue

            chair_name = aLink.text
            chair_link = aLink.get("href")

            # the link may be relative, so we need to add the prefix
            chair_link = _convert_to_full_url(chair_link)

            chair_link_touple_list.append((chair_name, chair_link))

    return chair_link_touple_list


class ChairParser:
    def __init__(self, chair_name):
        self.chair_name = chair_name

    """
    Parses the landing page of a chair.
    Returns the link to the team page of the chair.
    """

    def parse_landing_page(self, chair_link, chair_landing_page):
        soup = BeautifulSoup(chair_landing_page, "html.parser")

        # find the link to the chair's team page
        # the link can be found by looking for the first occurence of the text "team"
        # as the links can have different style, e.g. "Lehrstuhlteam" or "Team"
        # yes, this is an extreme hack, but it works

        link_to_team = None
        for link in soup.find_all("a"):
            if link.text.lower().find("team") != -1:
                link_to_team = link.get("href")
                break

        if link_to_team is None:
            raise Exception(f"{self.chair_name}: no link to team page found")

        return _convert_to_full_team_url(link_to_team, chair_link)

    """
    Parses the team page of a chair.
    Selects the correct parsing method based on the layout of the team page.
    """

    def parse_team_page(self, chair_team_page):
        # the team page layout can be different for each chair
        # select the correct parsing method based on the HTML tags and CSS classes used.

        if chair_team_page.find("table") != -1:
            return self.parse_table_layout_team_page(chair_team_page)
        else:
            logging.warning(f"{self.chair_name}: no team member table found. using mailtos")
            return self.parse_mailtos(chair_team_page)

    def parse_table_layout_team_page(self, chair_team_page):
        soup = BeautifulSoup(chair_team_page, "html.parser")

        member_names = []
        tables = []

        # the chair team members are in multiple tables
        # the tables cannot be simply found by their class or id
        # as such, we find the all tables in the <main> tag and look at all the links in the tables
        #
        # the links are the chair team members and their email addresses
        # we are only interested in the links that do not start with "mailto:"
        #
        # from the <a> we can get the names of the chair team members

        try:
            tables = soup.find("main").find_all("table")
        except Exception:
            pass
        if tables is None or len(tables) == 0:
            raise Exception("did not find any tables with team members (table layout)")

        try:
            for table in tables:
                for link in table.find_all("a"):
                    if link.get("href").find("mailto:") == -1:
                        member_names.append(link.text)
        except Exception:
            raise Exception("did not find any table with team members (table layout)")

        return member_names

    """
    Finds all member of staff in the chair team page by looking for mailto links.
    The mailto links contain the names of staff members, which are extracted.
    Invalid mailto links, i.e. containing html encoded tags for subject or body, are skipped.
    
    This methodology has the downside that student names are incorrectly extracted, as they only contain the last name.
    Note that they are not filtered out.
    """

    def parse_mailtos(self, chair_team_page):
        soup = BeautifulSoup(chair_team_page, "html.parser")

        # some email addresses are listed multiple times
        # using a set to avoid duplicates
        member_names = set()
        try:
            mailtos = soup.select("a[href^=mailto]")

            for mailto in mailtos:
                name = mailto["href"].split(":")[1]
                # skip email addresses that are not names
                if name.startswith("?"):
                    continue
                name = name.split("@")[0].replace(".", " ").title()

                member_names.add(name)
        except Exception as e:
            raise Exception(f"failed to extract mailtos: {e}")

        return list(member_names)
