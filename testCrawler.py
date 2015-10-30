from bs4 import BeautifulSoup
import urllib2
import itertools
import random
import urlparse


class Crawler(object):
    """docstring for Crawler"""

    # think about changing this to add new urls
    def __init__(self):
        self.soup = None                                        # Beautiful Soup object
        self.current_page   = "https://uoregon.edu/"          # Current page's address
        self.links          = set()                             # Queue with every links fetched
        self.visited_links  = set()

        self.counter = 0 # Simple counter for debug purpose

    def open(self):

        # Open url
        print self.counter , ":", self.current_page
        res = urllib2.urlopen(self.current_page)
        html_code = res.read()
        with open("/home/mebays/Documents/cs321/proj3/htmlFiles/uoregon" +
                  str(self.counter) + ".html", mode='w') as outfile:
            outfile.write(html_code)
            self.counter += 1
        self.visited_links.add(self.current_page)

        # Fetch every links
        self.soup = BeautifulSoup(html_code)
        print [h.get('href') for h in self.soup.find_all('a')]
        page_links = []
        try :
            for link in [h.get('href') for h in self.soup.find_all('a')]:
                if link is not None:
                    print "Found link: '" + link + "'"
                    if link.startswith('http') and u'uoregon.edu' in link:
                        page_links.append(link)
                        print "Adding link " + link + "\n"
                    elif link.startswith('//'):
                        parts = urlparse.urlparse(self.current_page)
                        page_links.append(parts.scheme + ':' + link)
                        print "Adding link " + parts.scheme + ':' + link + "\n"
                    elif link.startswith('/'):
                        parts = urlparse.urlparse(self.current_page)
                        page_links.append(parts.scheme + '://' + parts.netloc + link)
                        print "Adding link " + parts.scheme + '://' + parts.netloc + link + "\n"

        except Exception, ex: # Magnificent exception handling
            print ex

        # page_links is all links on page
        print len(page_links)
        # Update to unique links
        self.links = self.links.union( set(page_links) )

        # Choose a random url from non-visited set
        self.current_page = random.sample( self.links.difference(self.visited_links),1)[0]
        self.counter+=1

    def run(self):

        # Crawl 3 webpages (or stop if all url has been fetched)
        while (self.visited_links == self.links):
            self.open()

        print len(self.links)
        for link in self.links:
            print link

if __name__ == '__main__':
    C = Crawler()
    C.run()
