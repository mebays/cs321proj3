#!/bin/bash python

from bs4 import BeautifulSoup
import urllib2
import random
import urlparse
import time
import csv
import requests


class Crawler(object):

    '''Contructor '''
    def __init__(self):
        self.soup = None  # Beautiful Soup object
        self.current_page = "http://uoregon.edu/"  # Current page's address
        self.links = set()  # Queue with every links fetched
        self.visited_links = set()
        self.numberVisited = {}

        self.counter = 0  # Simple counter for debug purpose

    '''open url and acquire list of urls'''
    def open(self):

        # Open url
        print self.counter, ":", self.current_page
        # Try to open url incase there is a file extension it will through the
        # exception page Error for Error 404 or 500 data
        try:
            # html = requests.get(self.current_page).text
            res = urllib2.urlopen(self.current_page)
            html_code = res.read()
            self.visited_links.add(self.current_page)
            self.numberVisited[self.current_page] = 1
            # self.soup = BeautifulSoup(html)
            self.soup = BeautifulSoup(html_code)
        except:
            "page Error"
        # Fetch all Links
        page_links = []
        try:
            for link in [h.get('href') for h in self.soup.find_all('a')]:
                # check to avoid these in the link data
                if link is not None and u'calendar' not in link and u'.com' \
                        not in link and u'Shibboleth' not in link and u'.pdf' \
                        not in link and u'.gzip' not in link and u'.zip' \
                        not in link and u'.aspx' not in link \
                        and u'search' not in link \
                        and u'jobs' not in link \
                        and u'?' not in link \
                        and u'&' not in link \
                        and u'=' not in link \
                        and u'#' not in link:
                    print "Found link: '" + link + "'"

                    if link.startswith('http') and u'uoregon.edu' in link:
                        page_links.append(link)
                        print "Adding link" + link + "\n"

                    elif link.startswith('//'):
                        parts = urlparse.urlparse(self.current_page)
                        page_links.append(parts.scheme + ":" + link)
                        print "Adding link " + parts.scheme + ":" + link

                    elif link.startswith('/'):
                        parts = urlparse.urlparse(self.current_page)
                        page_links.append(parts.scheme + '://' +
                                          parts.netloc + link)
                        print "Adding link " + parts.scheme + '://' + \
                            parts.netloc + link + "\n"

                    else:
                        pass

        except Exception, ex:
            print ex

        # Checks if link is in Dictionary if so add 1 if not add it and place 1
        # for the count
        for link in page_links:
            if link in self.numberVisited:
                self.numberVisited[link] += 1
            else:
                self.numberVisited[link] = 1

        # Update the links data
        self.links = self.links.union(set(page_links))

        # Choose a random url from non-visited set
        self.current_page = random.sample(self.links.difference(
            self.visited_links), 1)[0]

        self.counter += 1

    def run(self):
        start = time.time()

        # Crawl 100 webpages (or stop if all url has been fetched)
        while len(self.visited_links) < 700 or \
                (self.visited_links == self.links):
            self.open()

        for link in self.links:
            print link
        
        csvFile = open("C:/Users/Matthew/Documents/CS321/cs321proj3" +
                       "/csvFiles/urlCSVdata.csv", mode="w")
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(['Id Number', 'Number of times',
                            'File Name', 'URL', 'title', 'text'])
        count = 0
        for link in self.links:
            try:
                # Replace special characters for a file Name
                fileName = link.replace(":", "").replace("/", "").\
                    replace(".", "").replace("?", "").replace("=", "").\
                    replace("&", "").replace("%", "")
                with open("C:/Users/Matthew/Documents/CS321/cs321proj3" +
                          "/htmlFiles/"+fileName+".txt", mode="w") as outfile:
                    result = urllib2.urlopen(link)
                    # result = requests.get(link).text
                    source_code = result.read()
                    outfile.write(source_code)
                    # outfile.write(result)

                soup_code = BeautifulSoup(source_code)
                # soup_code = BeautifulSoup(result)
                title = soup_code.title.string.encode('ascii', 'ignore')

                for script in soup_code(["script", "style"]):
                    script.extract()

                text = soup_code.get_text()
                csvWriter.writerow([count,
                                    self.numberVisited[link],
                                    fileName,
                                    link,
                                    title,
                                    text.encode('ascii', 'ignore')])
                count += 1

            except:
                pass

        csvFile.close()
        print len(self.links)
       
        print time.time()-start, 'seconds'

if __name__ == '__main__':
    C = Crawler()
    C.run()
