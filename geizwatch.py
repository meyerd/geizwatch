#!/usr/bin/python

# fetchesprice information for several products from
# the geizhals.at price comparison site
# each product number has to be listed in the file
# watched_products.txt (one product number per line)

BASE_URL = 'http://www.geizhals.at/deutschland'
NUM_PRICES = 5 # number of prices to show

consolewidth = 79
ratio = 1.0/4.0

leftlen = int(consolewidth * ratio)
rightlen = consolewidth - leftlen

import sys, os, re, textwrap
from WebCursor import WebCursor
from BeautifulSoup import BeautifulSoup
import HTMLParser
htmlparser = HTMLParser.HTMLParser()

def out(str):
    print >>sys.stdout, str

def error(str):
    print >>sys.stdout, str
    sys.exit(1)

if __name__ == '__main__':
    wpfile = open('watched_products.txt', 'r')
    if not wpfile:
        error('could not open watched_products.txt')

    product_numbers = []
    number_regex = re.compile('([0-9]*)')
    for line in wpfile:
        ret = number_regex.search(line)
        if ret:
            pid = ret.groups()[0].strip()
            if pid != '':
                product_numbers.append(pid)

    wc = WebCursor()

    for pid in product_numbers:
        url = BASE_URL + '/' + str(pid)
        page = wc.get(url)
        if page == '':
            error('could not download %s' % (url))
    
        soup = BeautifulSoup(page)
        hdr = soup.findAll('h1', attrs={'class':'arthdr'})[0]
        if not hdr:
            out('warning: error parsing product id %i' % (pid))
            continue
        product = hdr.findAll('span', attrs={'class':'notrans'})[0]
        if not product:
            out('warning: error parsing product id %i' % (pid))
            continue

        product = str(htmlparser.unescape(product.text)) + ': '

        prices = soup.findAll('span', attrs={'class':'price'})

        pricestr = ''

        c = 0
        for price in prices:
            if c > NUM_PRICES:
                break
            pricestr += str(htmlparser.unescape(price.text)) + ' '
            c += 1
       
        if len(product) < leftlen:
            product += (' ' * (len(product) - leftlen - 2))

        indentlen = 7

        wholestr = product + pricestr

        outstr = ('\n' + (' ' * (indentlen))).join(textwrap.wrap(wholestr, \
                                                             consolewidth-indentlen))
        out(outstr)


