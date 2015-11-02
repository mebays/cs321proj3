__author__ = 'mebays'

from bs4 import BeautifulSoup
import urllib2
import csv
import urlparse

class Crawler(object):

    def __init__(self):
        self.soup = None
        self.root_page = "https://uoregon.edu/"
        self.innerLinks = []
        self.links = set()
        self.visited_links = set()
        self.csvOutfile= open("C:\\Users\\mebays\\Documents\\cs321proj3\\csvFiles\\crawler.csv", mode='w')
        self.csvFile = csv.writer(self.csvOutfile)
        self.counter = 0

    def open(self):
        print self.counter, ':', self.root_page
        self.csvFile.writerow(['ID','filName','url'])
        self.writeHtml(self.root_page)


    def writeHtml(self, url):
        result = urllib2.urlopen(url)
        html_code = result.read()
        htmlFileName = url.replace("/","_").replace(".","_").replace(":","_")
        outfile = open("C:\\Users\\mebays\\Documents\\cs321proj3\\htmlFiles\\" +
                       htmlFileName + ".txt", mode='w')
        outfile.write(html_code)
        outfile.close()
        self.csvFile.writerow([self.counter, htmlFileName, url])
        self.counter += 1
        self.getLinks(url, html_code)

    def getLinks(self, netlocation, source_code):
        self.soup = BeautifulSoup(source_code)
        links = [h.get('href') for h in self.soup.find_all('a')]
        for link in links:
            self.checkInnerLinks(netlocation, link)

    def checkInnerLinks(self,root, link):
        if link is not None:
            print "Found link: '" + link + "'"
            if link.startswith('http') and u'uoregon.edu' in link:
                if link not in self.visited_links:
                    self.innerLinks.append(link)
                    self.csvFile.writerow([ self.counter, link.replace("/","_").replace(".","_").replace(":","_"), link])
                    print "Adding link " + link + "\n"
                    self.counter += 1
                    self.writeHtml(link)
            elif link.startswith('//'):
                parts = urlparse.urlparse(root)
                fullLink = parts.scheme + ":" + link
                if fullLink not in self.visited_links:
                    self.innerLinks.append(fullLink)
                    self.csvFile.writerow([ self.counter, fullLink.replace("/","_").replace(".","_").replace(":","_"), fullLink])
                    print "Adding link " + fullLink + "\n"
                    self.counter += 1
                    self.writeHtml(fullLink)
            elif link.startswith('/'):
                parts = urlparse.urlparse(root)
                fullLink = parts.scheme + "://" + parts.netloc + link
                if fullLink not in self.visited_links:
                    self.innerLinks.append(fullLink)
                    self.csvFile.writerow([ self.counter, fullLink.replace("/","_").replace(".","_").replace(":","_"), fullLink])
                    print "Adding link " + fullLink + "\n"
                    self.counter += 1
                    self.writeHtml(fullLink)


if __name__ == '__main__':
    C = Crawler()
    C.open()
