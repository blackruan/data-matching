'''
Extract semantic information from the Yelp pages
'''

#===============================================================================
# Total Att: 24, More biz info: 13
# Attribute list: ["name", "streetAddress", "city", "state", "zipCode", "telephone", 
# "website", "priceRange", "category", "ratingValue", "neighborhood", 
# "Takes Reservations", "Delivery", "Take-out", "Accepts Credit Cards", "Good For", 
# "Parking", "Attire", "Ambience", "Alcohol", "Outdoor Seating", "Wi-Fi", 
# "Waiter Service", "Caters"]
#===============================================================================

import csv
from bs4 import BeautifulSoup

cityList = ["new+york,ny","los+angeles,ca","chicago,il","houston,tx","philadelphia,pa", \
"phoenix,az","san+antonio,tx","san+diego,ca","dallas,tx","san+jose,ca"]

pre = "/Users/jinruan/Documents/15_fall/CS784/stage2/"
 
infoAttList = ["Takes Reservations", "Delivery", "Take-out", \
"Accepts Credit Cards", "Good For", "Parking", "Attire", "Ambience", "Alcohol", \
"Outdoor Seating", "Wi-Fi", "Waiter Service", "Caters"]

for c in cityList : 
     
    fcsv = open('yelp_' + c[:-3] + '.csv','wb')
    writer = csv.writer(fcsv, delimiter = ",")
     
    schema = ["name", "streetAddress", "city", "state", "zipCode", "telephone", 
    "website", "priceRange", "category", "ratingValue", "neighborhood", 
    "Takes Reservations", "Delivery", "Take-out", "Accepts Credit Cards", "Good For", 
    "Parking", "Attire", "Ambience", "Alcohol", "Outdoor Seating", "Wi-Fi", 
    "Waiter Service", "Caters"]
    writer.writerow(schema)
    
    f = open(pre + "yelp_" + c[:-3] + "/yelp_" + c + "_final.txt",'r')
    count = 0
    
    for line in f :
        page = open(pre + "yelp_" + c[:-3] + "/" + line[24:-1] + ".html", 'r')
        soup = BeautifulSoup(page.read(), "html.parser")
        page.close()
        
        s = []
        
        # search for name
        name = soup.find("h1", itemprop="name")
        s.append(name.string.strip().encode('utf-8'))
        
        mapbox = soup.find("div", class_="mapbox-text")
        
        # search for streetAddress 
        # <br> may occur in the street address
        streetAddress = mapbox.find("span", itemprop="streetAddress")
        addressSoup = BeautifulSoup(str(streetAddress).replace("<br>", " "), "html.parser")
        s.append(addressSoup.string.encode('utf-8'))
        
        # search for city
        city = mapbox.find("span", itemprop="addressLocality")
        s.append(city.string.encode('utf-8'))
        
        # search for state 
        state = mapbox.find("span", itemprop="addressRegion")
        s.append(state.string.encode('utf-8'))
        
        # search for zipCode 
        zipCode = mapbox.find("span", itemprop="postalCode")
        if (zipCode != None) :
            s.append(zipCode.string.encode('utf-8'))
        else :
            s.append("")
        
        # search for telephone
        telephone = mapbox.find("span", attrs={"class": "biz-phone", "itemprop": "telephone"})
        if (telephone != None) :
            s.append(telephone.string.strip().encode('utf-8'))
        else :
            s.append("")
        
        # search for website
        bizWebsite = mapbox.find("div", class_="biz-website")
        if (bizWebsite != None) :
            s.append(bizWebsite.a.string.encode('utf-8'))
        else :
            s.append("")    
        
        mainInfo = soup.find("div", class_="biz-main-info embossed-text-white")
    
        # search for price range
        priceRange = mainInfo.find("span", attrs={"class": "business-attribute price-range", \
        "itemprop": "priceRange"})
        if (priceRange != None) :
            s.append(priceRange.string.encode('utf-8'))
        else :
            s.append("")  
        
        # search for category
        categoryList = mainInfo.find("span", class_="category-str-list").find_all("a")
        if (categoryList) :  
            category = categoryList[0].string
            for index in range(1, len(categoryList)):
                category = category + ';' + categoryList[index].string
            s.append(category.encode('utf-8'))
        else :
            s.append("")
        
        # search for ratingValue
        ratingValue = mainInfo.find("meta", itemprop="ratingValue")
        if (ratingValue != None) :
            s.append(ratingValue['content'].encode('utf-8'))
        else :
            s.append("")
        
        # search for neighborhood
        neighborhood = mapbox.find("span", class_="neighborhood-str-list")
        if (neighborhood != None) :
            s.append(neighborhood.string.replace(",", ";").strip().encode('utf-8'))
        else :
            s.append("")
        
        # search for more biz info
        moreBizInfoSoup = soup.find("div", class_="short-def-list")
        if (moreBizInfoSoup != None) :
            info = {}
            for i in moreBizInfoSoup.find_all("dl") :
                info[i.find("dt").string.strip()] = i.find("dd").string.strip()
            for infoAtt in infoAttList :
                if (infoAtt in info) : 
                    s.append(info[infoAtt].replace(",", ";").encode('utf-8'))
                else :
                    s.append("")
        else :
            for infoAtt in infoAttList :
                s.append("")
    
        count += 1
        print count
        writer.writerow(s)
    
    f.close()
    fcsv.close()