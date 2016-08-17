'''
Save the urls of the web pages into txt files
'''
import re
import urllib2
from time import sleep

keyword = "restaurants"
city = ["new+york,ny","los+angeles,ca","chicago,il","houston,tx","philadelphia,pa",\
       "phoenix,az","san+antonio,tx","san+diego,ca","dallas,tx","san+jose,ca"]

yelp_offset = 10
num = 100

for c in city :
    output_file = "yelp_" + c + ".txt"
    f = open(output_file, 'w')

    for o in range(num):
        links = "http://www.yelp.com/search?find_desc="+ \
            keyword + "&find_loc=" + c + "&start=" + str(o * yelp_offset)
        print(links)
        page = urllib2.urlopen(links)
        page_content = page.read()
        urls = re.findall(r"<a.*?\s*href=\"(.*?)\".*?>(.*?)</a>", page_content)
    
        i= 0
        for u in urls:
            if "/biz/" in u[0] and i< 10:
                i += 1
                f.write("http://www.yelp.com" + u[0] + "\n")
        
        sleep(5)
    
    f.close()