__author__ = 'mebays'

#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib2
import itertools
import random
import urlparse
import time
import csv


class Crawler(object):
    """docstring for Crawler"""

    def __init__(self):
        self.soup = None                                        # Beautiful Soup object
        self.current_page   = "http://uoregon.edu/"          # Current page's address
        self.links          = set()                             # Queue with every links fetched
        self.visited_links  = set()

        self.counter = 0 # Simple counter for debug purpose

    def open(self):

        # Open url
        print self.counter , ":", self.current_page
        try:
            res = urllib2.urlopen(self.current_page)
            html_code = res.read()
            self.visited_links.add(self.current_page)

        # Fetch every links
            self.soup = BeautifulSoup(html_code)
        except:
            "page Error"

        page_links = []
        try :
            for link in [h.get('href') for h in self.soup.find_all('a')]:
                if link is not None and u'calendar' not in link and u'.com' not in link and u'Shibboleth' not in link and u'.pdf' not in link and u'.gzip' not in link and u'.zip' not in link and u'.aspx' not in link:
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
                        page_links.append(parts.scheme + '://' + parts.netloc + link)
                        print "Adding link " + parts.scheme + '://' + parts.netloc + link + "\n"
                    else:
                        pass

        except Exception, ex: # Magnificent exception handling
            print ex

        # Update links
        self.links = self.links.union( set(page_links) )

        # Choose a random url from non-visited set
        self.current_page = random.sample( self.links.difference(self.visited_links),1)[0]
        self.counter+=1

    def run(self):
        start = time.time()
        # Crawl 3 webpages (or stop if all url has been fetched)
        while len(self.visited_links) < 100 or (self.visited_links == self.links):
            self.open()

        for link in self.links:
            print link
        csvFile = open("C:\\Users\\Matthew\\Documents\\CS321\\cs321proj3\\csvFiles\\csvData.csv", mode="w")
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(['Id Number', 'File Name', 'URL', 'title', 'text'])
        count = 0
        for link in self.links:
            try:
                fileName = link.replace(":","_").replace("/","_").replace(".","_").replace("?","-").replace("=","-").replace("&","_").replace("%","_")
                with open("C:\\Users\\Matthew\\Documents\\CS321\\cs321proj3\\htmlFiles\\"+fileName+".txt", mode="w") as outfile:
                    result = urllib2.urlopen(link)
                    source_code = result.read()
                    outfile.write(source_code)
		    soup_code = BeautifulSoup(source_code)
		    title = soup_code.title.string.encode('ascii', 'ignore')
		    for script in soup_code(["script", "style"]):
			    script.extract()
			    
		text = soup_code.get_text().replace("\n", " ")					
                csvWriter.writerow([count, fileName, link, title, text.encode('ascii', 'ignore')])
                count += 1
            except:
                pass

        csvFile.close()
        print len(self.links)
        print time.time()-start, 'seconds'

if __name__ == '__main__':
    C = Crawler()
    C.run()
