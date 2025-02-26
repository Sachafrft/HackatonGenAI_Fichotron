from bs4 import BeautifulSoup
import requests
list_site=[]


ville="dijon"
## LISTES DES THEMES GOOGLE A RECHERCHER A CHAQUE FOIS
param=["budget","orientation budgetaire","transition écologique","projet education","maire","urbanisme",'aménagement','investissement']

### REQUETE POUR AVOIR LES URLS PRINCIPALE : MAIRIE ET WIKIPEDIA
requete_main=f"ville inurl:{ville}"



from googlesearch import search
from time import sleep
def get_url(recherche):
    all_url = []
    for url in search(recherche, num_results=10, lang="fr"):
        sleep(0.5)
        if ('google.com' not in url) and ("jpg" not in url) and ("Portail" not in url):
            all_url.append(url)
    return all_url

### PRISE DES SOUS URL RECENTES SELON UN THEME PRECIS
def get_sous_url(main_url,theme):
    sous_urls=get_url(f"site:{main_url} {theme} after:2023-01-01")
    return sous_urls


#### URL WIKIPEDIA
requete_wiki1=f"ville {ville} wikipedia"
requete_wiki2=f"metropole {ville} wikipedia"

# url wiki commune => avoir donnee maire
url_wiki1=get_url(requete_wiki1)[0]
#metropole => url wiki metropole
url_wiki2=get_url(requete_wiki2)[0]


### ajout lien wikipedia
list_site.append(url_wiki1)
list_site.append(url_wiki2)



### URL SITE PRINCIPAL
url_main=get_url(requete_main)[0]
list_site.append(url_main)

### CREATION D'URLS ET AJOUT A LA LISTE D'URLS
for ele in param:
    urls=get_sous_url(url_main,ele)
    for lien in urls:
        list_site.append(lien)

## LIENS API POUR AVOIR LES DONNEES DE DATA GOUV
url_gouv1=f"https://data.ofgl.fr/api/explore/v2.1/catalog/datasets/ofgl-base-communes-consolidee/records?where=exer%20%3E%20date%272022%27%20and%20(%20%20(agregat%20like%20%27Epargne%20brute%27)%20or%20(agregat%20like%20%27Epargne%20nette%27)%20or%20(agregat%20like%20%27Epargne%20gestion%27)%20)%20%20and%20com_name%20like%20%27{ville}%27&limit=100"
url_gouv2=f"https://data.ofgl.fr/api/explore/v2.1/catalog/datasets/ofgl-base-gfp/records?where=exer%20%3E%20date%272022%27%20and%20(%20%20(agregat%20like%20%27Recettes%20de%20fonctionnement%27)%20or%20(agregat%20like%20%27Encours%20de%20dette%27)%20)&limit=100"

