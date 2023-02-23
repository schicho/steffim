import fimparser

def main():
    # open the chairs.html file
    with open('chairs.html') as f:
        # read the file
        html = f.read()
        # parse the html
        links = fimparser.parse_chair_page(html)
        # print the links
        print(links)

if __name__ == '__main__':
    main()
