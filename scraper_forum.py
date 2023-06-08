import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
from datetime import datetime
import sys

### Parameters ###
nb_categories = -1
nb_pages = -1
nb_posts_per_page = -1

sleep_time = 1  # sleep time between requests
###

RESET = "\033[0m"
RED = "\033[31m"

tree_info = ET.parse('info_site.xml')
root_info = tree_info.getroot()
# Retrieve elements
main_link = root_info.find('lien_site').text + "/forum"


def get_all_links(page):
    urls = [link.get('href') for link in page.select('span.title a')]
    return urls


def get_themes(page):
    themes_urls = [link.get('href') for link in page.select('div[class *= "view-liste-des-themes"] span.field-content a')]
    return themes_urls


def number_of_pages(page):
    last_page_element = page.find("li", {"class": "pager-last last"})
    if last_page_element:
        last_page_link = last_page_element.find("a")["href"]
        last_page_number = int(last_page_link.split("=")[-1])
        return last_page_number
    else:
        return 0


def get_title(page):
    title = page.find('h2', class_='sub-title-forum')
    print(title.text)
    return title.text


def get_post(page):
    post = page.select('div[typeof="sioc:Post sioct:BoardPost"] div.field-item.even')
    return post[0].text


def get_comments(page):
    comments = page.select('div#forum-comments div.field-item.even ')
    return [com.text for com in comments]


def add_list_to_xml(name, parent, liste):
    liste_branches = []
    for elem in liste:
        branch = ET.SubElement(parent, name)
        branch.text = elem
        liste_branches.append(branch)
    return liste_branches

def my_request(link):
    time.sleep(sleep_time)
    return requests.get(link)


def main(file_name, nb_categories, nb_pages, nb_posts_per_page):
    start_time = time.time()
    root = ET.Element('forum')
    response = my_request(main_link)
    soup = BeautifulSoup(response.content, 'lxml')

    theme_list = get_themes(soup)
    simple_theme_list = [t.split("/")[2].replace("-", " ") for t in theme_list]
    date_branch = ET.SubElement(root, "date")
    date_branch.text = str(datetime.now())

    category_branches = ET.SubElement(root, "categories")
    liste_branch_theme = []#add_list_to_xml_id("categorie", category_branches, simple_theme_list)

    base_link = "/".join(main_link.rsplit("/")[:-1])

    nb_categories_i = len(theme_list) if nb_categories == -1 else nb_categories
    for nt in range(nb_categories_i):
        theme_link = base_link + theme_list[nt]

        page_theme = my_request(theme_link)
        soup_theme = BeautifulSoup(page_theme.content, 'lxml')
        nb_page_theme = number_of_pages(soup_theme)

        liste_links_posts = get_all_links(soup_theme)
        nb_pages_i = nb_page_theme + 1 if nb_pages == -1 else nb_pages
        
        branch = ET.SubElement(category_branches, "categorie")
        branch_name = ET.SubElement(branch, "nom")
        branch_name.text = simple_theme_list[nt]
        liste_branch_theme.append(branch)
        
        branch_posts = ET.SubElement(liste_branch_theme[nt], "postes")
        for n in range(nb_pages_i):
            page_theme_n = my_request(theme_link + "?page=" + str(n))
            soup_theme_n = BeautifulSoup(page_theme_n.content, 'lxml')
            
            liste_links_posts_n = get_all_links(soup_theme_n)[1:]
            Listes_branch_posts_p = []#add_list_to_xml_simple("poste", branch_posts, liste_links_posts_n[1:])
            nb_posts_per_page_i = len(liste_links_posts_n) if nb_posts_per_page == -1 else nb_posts_per_page

            for l in range(nb_posts_per_page_i):
                post_link = base_link + liste_links_posts_n[l]
                page_post = my_request(post_link)
                soup_post = BeautifulSoup(page_post.content, 'lxml')

                
                branch = ET.SubElement(branch_posts, "poste")
                Listes_branch_posts_p.append(branch)
                
                branch_post = Listes_branch_posts_p[l]
                title = get_title(soup_post)
                branch_title = ET.SubElement(branch_post, "titre")
                branch_title.text = title

                nb_pages_post = number_of_pages(soup_post)
                branch_nb_pages_post = ET.SubElement(branch_post, "nb_pages")
                branch_nb_pages_post.text = str(nb_pages_post)

                post = get_post(soup_post)
                branch_text_post = ET.SubElement(branch_post, "texte_poste")
                branch_text_post.text = post

                branch_comments = ET.SubElement(branch_post, "commentaires")
                comments_page0 = get_comments(soup_post)
                add_list_to_xml("commentaire", branch_comments, comments_page0)

                for p in range(1, nb_pages_post):
                    post_link_p = post_link + "?page=" + str(p)
                    page_post_n = my_request(post_link_p)
                    soup_post_n = BeautifulSoup(page_post_n.content, 'lxml')

                    comments = get_comments(soup_post_n)
                    add_list_to_xml("commentaire", branch_comments, comments)

    end_time = time.time()
    execution_time = end_time - start_time
    print()

    if execution_time <= 60:
        print("The code executed in", RED + str(execution_time), RESET + "seconds.")
    elif execution_time <= 60 * 60:
        print("The code executed in", RED + str(execution_time / 60), RESET + "minutes.")
    else:
        print("The code executed in", RED + str(execution_time / 3600), RESET + "hours.")

    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_string = ET.tostring(root, encoding="unicode", method="xml", short_empty_elements=False)

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(xml_declaration + xml_string)


if __name__ == "__main__":
    try:
        print(sys.argv[1])
    except:
        print(f"Warning: no file name specified.")
        exit(1)
    main(sys.argv[1], nb_categories, nb_pages, nb_posts_per_page)
