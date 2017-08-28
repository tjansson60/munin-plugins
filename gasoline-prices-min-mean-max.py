#!/usr/bin/env python

import sys
import urllib2
from BeautifulSoup import BeautifulSoup

# Get the website that will be scraped into a varialbe
websiteurl = "http://www.fdmbenzinpriser.dk/searchprices/2/K%C3%B8benhavn"
soup       = BeautifulSoup(urllib2.urlopen(websiteurl).read())

# Make a list of all the prices
prices = []
for price in str(soup.findAll('td', attrs={'class' : 'tablebodyprice'})).split('class="octanelink">')[1:]:
    if '*' in price.split('</a></td>')[0]:
        prices.append(float(price.split('</a></td>')[0].split('*')[0].strip()))
    else:
        prices.append(float(price.split('</a></td>')[0]))

# Sanity check to remove prices lower than 5kr/l.
prices = [ price for price in prices if price > 5 ]

# Find the minimum, maximum and mean prices 
minval  = min(prices)
maxval  = max(prices)
minval2 = 8.5
maxval2 = 13.5
mean    = sum(prices, 0.0)/len(prices)

# Define the details of the graph
if len(sys.argv) > 1 and sys.argv[1] == "config":
    print "graph_title Gasoline price for Blyfri 95 in Copenhagen based on "+str(len(prices))+" prices."
    print "graph_args --base 1000 --rigid -l "+str(minval2)+" -u "+str(maxval2)
    print "graph_vlabel DKK/L"
    print "graph_category other"
    print "graph_info Gasoline prices for Blyfri 95 in the Copenhagen area. Prices scraped from: "+websiteurl
    print "minimum.label Minimum value"
    print "maximum.label Maximum value"
    print "mean.label Mean of all "+str(len(prices))+" prices."
    sys.exit()

# Print the values when munin calls the script. 
print "minimum.value "+str(minval)
print "maximum.value "+str(maxval)
print "mean.value "+str(mean)
