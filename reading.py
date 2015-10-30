from dataCollection import Readurl

# start over with the main method dataCollection is deleted and should be using
# only the testCrawler after minipulating the style should work well.

def main():
    start = Readurl()
    start.read()
    allLinks = start.findLinks()
    newLinks = []

    for link in allLinks:
        try:
            if link and link.startswith('//'):
                prefixLink = 'http:' + link
                start.setUrl(prefixLink)
                start.read()
                newLinks.appen(start.findLinks())

            elif link and links.startswith('/'):
            else:
                start.setUrl('http://uoregon.com' + link)
                start.read()
                newLinks.appen(start.findLinks())
        except:
            print link

    print allLinks
    print newLinks


if __name__ == '__main__':
    main()
