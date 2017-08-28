#!/usr/bin/env python

import sys
import urllib2
from BeautifulSoup import BeautifulSoup

# Get the website that will be scraped into a varialbe
websiteurl     = "http://www.fdmbenzinpriser.dk/searchprices/2/K%C3%B8benhavn"
soup           = BeautifulSoup(urllib2.urlopen(websiteurl).read())
vendorprice    = {}
vendornumber   = {}
allowedvendors = ['ok', 'shell', 'jet', 'q8', 'statoil']

# Make a list of all the prices
vendors = []
for vendor in str(soup.findAll('td', attrs={'class' : 'tablebodyprice'})).split('<a href="/')[1:]:
    vendorstripped = vendor.split('/')[0]
    if vendorstripped not in vendors and vendorstripped in allowedvendors:
        vendors.append(vendorstripped)

rawsoup = soup.findAll('td', attrs={'class' : 'tablebodyprice'})
for vendor in vendors:
    prices = []
    number = 0
    for element in rawsoup:
        if vendor in str(element):
            elementraw = str(element).split('class="octanelink">')[1].split('</a></td>')[0]
            if '*' in elementraw:
                prices.append(float(elementraw.split('*')[0].strip()))
            else:
                prices.append(float(elementraw))
            number = number+1

    # Sanity check to remove prices lower than 5kr/l.
    prices = [ price for price in prices if price > 5 ]

    if len(prices) == 0:
        mean = None
    else:
        mean   = sum(prices, 0.0)/len(prices)
    vendorprice[vendor]=mean
    vendornumber[vendor]=number

# Find the minimum, maximum for the plotting
allprices = []
for vendor in vendors:
    allprices.append(float(vendorprice[vendor]))

minval = int(min(allprices))+1
maxval = int(max(allprices))+1
minval = 8.5
maxval = 13.5


# Define the details of the graph
if len(sys.argv) > 1 and sys.argv[1] == "config":
    print "graph_title Mean gasoline price for Blyfri 95 per vendor in Copenhagen"
    print "graph_args --base 1000 --rigid -l "+str(minval)+" -u "+str(maxval)
    print "graph_vlabel DKK/L"
    print "graph_category other"
    print "graph_info Gasoline prices for Blyfri 95 in the Copenhagen area. Prices scraped from: "+websiteurl
    for vendor in vendors:
        print vendor+".label mean "+vendor+" price based on "+str(vendornumber[vendor])+" values"
    sys.exit()

# Print the values when munin calls the script.
for vendor in vendors:
    print vendor+".value "+str(vendorprice[vendor])
