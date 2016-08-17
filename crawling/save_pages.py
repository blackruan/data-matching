'''
Crawl the pages of the previous saved urls from websites
'''

import os
import urllib2
from time import sleep

input_file = "yelp_san+diego/yelp_san+diego,ca_final.txt"
f = open(input_file, 'r')
counter = 0

for line in f :
    page = urllib2.urlopen(line[:-1])
    page_content = page.read()
    s = line[24:-1]
    with open("yelp_san+diego/" + s + ".html", 'w') as fid:
        fid.write(page_content)
    print "%d: %s" % (counter, s)
    if (os.stat("yelp_san+diego/" + s + ".html").st_size < 102400) :
        print "blocked by Yelp"
        break
    counter += 1
    sleep(4)