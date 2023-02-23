import fimparser

def main():
    # open the chairs.html file
    with open('htmls/chairs.html') as f:
        # read the file
        html = f.read()
        # parse the html
        links = fimparser.parse_chair_page(html)
        # print the links
        print(links)

def parse_landingpage(filename):
    with open(filename) as f:
        # read the file
        html = f.read()
        # parse the html
        name, link = fimparser.parse_chair_landingpage(html)
        # print the name and link
        print(name, link)

if __name__ == '__main__':
    main()
    parse_landingpage('htmls/landing-dke.html')
    parse_landingpage('htmls/landing-tech.html')
