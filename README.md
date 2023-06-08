# scraper_python_site_santee

Ce projet a été réalisé dans le cadre d'un projet scolaire et vise à extraire les données d'un forum en utilisant des requêtes HTTP et le module BeautifulSoup. L'objectif principal est de récupérer les titres, les contenus des messages et les commentaires des publications du forum.

Veuillez noter que le nom du site a été omis dans ce README pour des raisons de confidentialité et de sécurité. Afin de ne pas interférer avec le fonctionnement normal du site, **les informations permettant d'accéder au site ont été séparées dans un autre fichier qui n'est pas inclus. Par conséquent, le projet ne fonctionnera pas sous la forme présentée ici.** Je tiens à souligner que je respecte les politiques d'utilisation du site et queje ne cherche en aucun cas à perturber son fonctionnement normal. Des mesures ont été prises pour éviter toute utilisation abusive ou spam de requêtes.

## Bibliothèques utilisées

- [requests](https://pypi.org/project/requests/): Pour effectuer des requêtes HTTP vers le forum.
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/): Pour analyser le HTML et extraire les données du forum.
- [xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html): Pour générer le fichier XML de sortie.
- [datetime](https://docs.python.org/3/library/datetime.html): Pour enregistrer la date et l'heure de l'exécution du script.
- [sys](https://docs.python.org/3/library/sys.html): Pour récupérer les arguments en ligne de commande.

## Paramètres

Je peux ajuster les paramètres suivants dans le fichier `main.py` pour personnaliser le processus d'extraction :

- `nb_categories`: Le nombre de catégories de forum à extraire. Utilisez -1 pour toutes les catégories.
- `nb_pages`: Le nombre de pages à extraire par catégorie. Utilisez -1 pour toutes les pages.
- `nb_posts_per_page`: Le nombre de publications à extraire par page. Utilisez -1 pour toutes les publications.
- `sleep_time` : Temps entre les requettes.

## Résultats 
Le résultat est un fichier XML dont vous pouvez choisir le nom au début du programme. Voici les DTD (Document Type Definitions) des deux scrapers :
Forum:

```
<xml version "1.0">
<!ELEMENT forum (date, categories)>
<!ELEMENT date (#PCDATA)>
<!ELEMENT categories (categorie+)>
<!ELEMENT categorie (nom, postes)>
<!ELEMENT nom (#PCDATA)>
<!ELEMENT postes (poste+)>
<!ELEMENT poste (titre, nb_pages, texte_poste, commentaires?)>
<!ELEMENT titre (#PCDATA)>
<!ELEMENT nb_pages (#PCDATA)>
<!ELEMENT texte_poste (#PCDATA)>
<!ELEMENT commentaires (commentaire+)>
<!ELEMENT commentaire (#PCDATA)>

```
TDC:

```
<xml version "1.0">
<!ELEMENT informations (date, types_de_cancer)>
<!ELEMENT date (#PCDATA)>
<!ELEMENT types_de_cancer (type_de_cancer+)>
<!ELEMENT type_de_cancer (type, texte_principal, articles)>
<!ELEMENT type (#PCDATA)>
<!ELEMENT texte_principal (#PCDATA)>
<!ELEMENT articles (article*)>
<!ELEMENT article (titre, texte)>
<!ELEMENT titre (#PCDATA)>
<!ELEMENT texte (#PCDATA)>

```
