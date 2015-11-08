#! /usr/bin/python
from urllib import *
from bs4 import BeautifulSoup
import sys
import json

searches = sys.argv[2:]
pages = sys.argv[1]

urls = []
i = 0
media_links = open('media_links', 'w')
for search in searches:
    print "BUSCANDO RESULTADOS PARA: " + search
    uri = 'https://twitter.com/i/search/timeline?f=tweets&vertical=default&q=' + search + '&include_available_features=1&include_entities=1&max_position=TWEET-6'
    for z in range(int(pages)):
        bundle = urlopen(uri).read()
        jtxt = json.loads(bundle)
        html = jtxt['items_html']
        minTweet = jtxt['min_position']
        print minTweet
        last_uri = uri
        uri = 'https://twitter.com/i/search/timeline?f=tweets&vertical=default&q=' + search + '&include_available_features=1&include_entities=1&max_position=' + minTweet
        if uri == last_uri:
            print "No hay mas resultados"
            media_links.close()
            sys.exit(0)
        soup = BeautifulSoup(html, "lxml")
        #print soup.prettify()
        elements = [x for x in soup.html.body.contents if x.name == 'li']
        for element in elements:
            name = element.div['data-screen-name']
            content = element.find('div', class_='content')
            media = content.find('div', class_='js-old-media-container')
            if not media:
                media = content.find('div', class_='js-media-container')
            if not media:
                print "Usuario sin media: " + name
            else: # hay media
                multi_photos = media.find('div', class_='multi-photos')
                
                if multi_photos: # multifoto
                    print "Usuario: " + name + " multifoto"
                    for image in multi_photos.find_all('img'):
                        if image['src'] + ':large' not in urls:
                            file = open(str(i) +".jpg", "w")
                            file.write(urlopen(image['src'] + ':large').read())
                            urls.append(image['src'] + ':large')
                            file.close()
                            print "Descargando imagen " + str(i) + ".jpg"
                            i+=1
                        else:
                            print "Imagen " + image['src'] + ':large' + " repetida"
                else: # otro media
                    images = media.findAll('div', class_='js-old-photo')
                    print "Usuario: " + name
                    if len(images) > 0: # image simple
                        for a in images:
                            image = a['data-image-url']
                            if image + ':large' not in urls:
                                file = open(str(i) +".jpg", "w")
                                file.write(urlopen(image + ":large").read())
                                urls.append(image)
                                file.close()
                                print "Descargando imagen " + str(i) + ".jpg"
                                i+=1
                            else:
                                print "Imagen " + image + " repetida"
                        
                    else: # video o foto externa
                        card = media.find('div', class_='js-macaw-cards-iframe-container')
                        if card:   
                            url = 'https://twitter.com' + card['data-src']
                            if url not in urls:
                                urls.append(url)
                                print "Media URL: " + url
                                media_links.write(url + '\n')
                            else:
                                print "Media URL: " + url + " repetida"
media_links.close()

