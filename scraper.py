import json
import requests
from lxml import html

with open("info_site.json") as my_file:
    json_str = my_file.read()

py_dict = json.loads(json_str)
type(py_dict)

#informations
lien = py_dict["lien_site"]
cats = py_dict["liste_categorie"]

response = requests.get(lien)
# Parser le contenu HTML avec lxml
tree = html.fromstring(response.content)
# Trouver la balise particulière que vous voulez récupérer
#tag = tree.xpath('//div[@class="field-item even"]')
title = tree.xpath('//h2[@class="sub-title-forum"]')
#post = tree.xpath('/div[@typeof="sioc:Post\ sioct:BoardPost"]//div[@class="field-item even"]')
post = tree.xpath('//div[contains(@typeof, "sioc:Post sioct:BoardPost")]//div[@class="field-item even"]')

"""
tag = tree.xpath('//div[@typeof="sioc:Post sioct:BoardPost"]')[0]
post = tag.xpath('//div[@class="field-item even"]')

print(post[0].text_content())
""""""
tag = tree.get_element_by_id("forum-comments")
#tag = tree.xpath('//div[@typeof="sioc:Post sioct:Comment"]')[0]
post = tag.xpath('//div[@class="field-item even"]')"""
comments = tree.xpath('//div[@id="forum-comments"]//div[@class="field-item even"]')

print(post[0].text_content())

#print(title[0].text_content())
