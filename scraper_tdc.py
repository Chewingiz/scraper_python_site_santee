import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
from datetime import datetime
import sys

sleep_time = 1  # sleep time between requests

RESET = "\033[0m"
RED = "\033[31m"

tree_info = ET.parse('info_site.xml')
root_info = tree_info.getroot()

# Get elements
lien_principal = root_info.find('lien_site').text
lien_base_article = root_info.find('lien_base_article').text

def get_links_and_titles(page):
    links_titles = page.select_one('.menu-block-6')
    lt_list = []
    li_elements = links_titles.find_all('li')
    for elem in li_elements:
        link = elem.find('a').get('href')
        text = elem.find('a').text
        # print(link)
        # print(text)
        lt_list.append([link, text])
    return lt_list[1:]

def get_categories(page):
    categories = page.find_all('div', class_='content-localisation')
    C_list = []
    for category in categories:
        title = category.find('h2', class_='title-localisation').text
        text_base = category.find('span', class_='desc-localisation')
        text = ''
        for part in text_base:
            text += part.text
        # print(f'Title: {title}')
        # print(f'Text: {text}\n')
        C_list.append([title, text])
    return C_list

def get_main_text(page):
    text = page.select_one('.field-item').text
    # print(f'Text: {text}')
    return text

def my_request(link):
    time.sleep(sleep_time)
    return requests.get(link)

def main(file_name):
    start_time = time.time()

    root = ET.Element('informations')

    date_branch = ET.SubElement(root, "date")
    date_branch.text = str(datetime.now())

    response = my_request(lien_principal + lien_base_article)
    # print(lien_principal + lien_base_article)
    soup = BeautifulSoup(response.content, 'lxml')

    links_and_titles = get_links_and_titles(soup)
    types_of_cancer_branch = ET.SubElement(root, "types_de_cancer")

    for lat in links_and_titles:
        title = lat[1]
        link = lat[0]
        branch = ET.SubElement(types_of_cancer_branch, "type_de_cancer")

        type_branch = ET.SubElement(branch, "type")
        type_branch.text = title
        print(title)

        response2 = my_request(lien_principal + link)

        soup2 = BeautifulSoup(response2.content, 'lxml')

        main_text = get_main_text(soup2)
        main_text_branch = ET.SubElement(branch, "texte_principal")
        main_text_branch.text = main_text

        articles = get_categories(soup2)
        articles_branch = ET.SubElement(branch, "articles")
        for art in articles:
            article_title = art[0]
            article_text = art[1]
            article_branch = ET.SubElement(articles_branch, "article")

            article_title_branch = ET.SubElement(article_branch, "titre")
            article_title_branch.text = article_title

            article_text_branch = ET.SubElement(article_branch, "texte")
            article_text_branch.text = article_text

    # Pause
    end_time = time.time()
    # Execution time
    execution_time = end_time - start_time
    print("\nThe code executed in", RED + str(execution_time), RESET + "seconds.")

    # Convert the tree to a string and write it to a file
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_string = ET.tostring(root, encoding="unicode", method="xml", short_empty_elements=False)
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(xml_declaration + xml_string)

# "Types_cancer.xml"
if __name__ == "__main__":
    try:
        print(sys.argv[1])
    except:
        print(f"Warning: no file name specified.")
        exit(1)
    main(sys.argv[1])
