from mainCrawler import Crawler
# start over with the main method dataCollection is deleted and should be using
# only the testCrawler after minipulating the style should work well.


def main():
    count = 0
    main = Crawler('https://uoregon.edu/')
    count += 1
    uniqMain, allMain = main.run()
    travelUniqLinks = []
    travelallLinks = []
    travelUniqLinks.append(uniqMain)
    travelallLinks.append(allMain)
    for link in uniqMain:
        try:
            oneDeep = Crawler(link)
            uniq1, allTravel1 = oneDeep.run()
            travelUniqLinks.append(uniq1)
            travelallLinks.append(allTravel1)
            count += 1
            for link2 in uniq1:
                try:
                    twoDeep = Crawler(link2)
                    uniq2, allTravel2 = twoDeep.run()
                    travelUniqLinks.append(uniq2)
                    travelallLinks.append(allTravel2)
                    count += 1
                except:
                    pass

        except:
            pass

    print len(travelUniqLinks)
    for links in travelUniqLinks:
        print len(links)
    print "the uniq List of links\n\n", travelUniqLinks
    print "the list of links \n\n", travelallLinks
    print len(travelallLinks)
    total = len(travelallLinks)
    for links in travelallLinks:
        total += len(links)

    print total
    total = len(travelUniqLinks)
    for links in travelUniqLinks:
        total += len(links)

    print total


if __name__ == '__main__':
    main()
