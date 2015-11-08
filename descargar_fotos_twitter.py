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
    uri = 'https://twitter.com/i/search/timeline?f=realtime&q=' + search + '&src=typd&include_available_features=1&include_entities=1'
    for z in range(int(pages)):
        bundle = urlopen(uri).read()
        jtxt = json.loads(bundle)
        html = jtxt['items_html']
        scroll_cursor = jtxt['scroll_cursor']
        #print scroll_cursor
        last_uri = uri
        uri = 'https://twitter.com/i/search/timeline?f=realtime&q=' + search + '&src=typd&include_available_features=1&include_entities=1&scroll_cursor=' + scroll_cursor
        if uri == last_uri:
            print "No hay mas resultados"
            media_links.close()
            sys.exit(0)
        soup = BeautifulSoup(html)
        elements = [x for x in soup.html.body.contents if x.name == 'li']
        for element in elements:
            name = element.div['data-screen-name']
            content = element.find('div', class_='content')
            media = content.find('div', class_='js-media-container')
            if not media:
                print "Usuario sin media: " + name
            else: # hay media
                multi_photos = media.find('div', class_='multi-photos')
                
                if multi_photos: # multifoto
                    print "Usuario: " + name + " multifoto"
                    for image in multi_photos.find_all('div'):
                        if image['data-resolved-url-large'] + ':large' not in urls:
                            file = open(str(i) +".jpg", "w")
                            file.write(urlopen(image['data-resolved-url-large'] + ':large').read())
                            urls.append(image['data-resolved-url-large'] + ':large')
                            file.close()
                            print "Descargando imagen " + str(i) + ".jpg"
                            i+=1
                        else:
                            print "Imagen " + image['data-resolved-url-large'] + ':large' + " repetida"
                else: # otro media
                    a = media.find('a', class_='media')
                    print "Usuario: " + name
                    if a: # image simple
                        image = a['data-url']
                        if image not in urls:
                            file = open(str(i) +".jpg", "w")
                            file.write(urlopen(image).read())
                            urls.append(image)
                            file.close()
                            print "Descargando imagen " + str(i) + ".jpg"
                            i+=1
                        else:
                            print "Imagen " + image + " repetida"
                        
                    else: # video o foto externa
                        url = media.div['data-card-url']
                        if url not in urls:
                            urls.append(url)
                            print "Media URL: " + url
                            media_links.write(url + '\n')
                        else:
                            print "Media URL: " + url + " repetida"
media_links.close()

