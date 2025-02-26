import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1').text # .text permet d'enlever toutes les balises html
    all_text = [line.strip() for line in soup.text.splitlines() if line.strip()]
    #title et all_text sont des string
    return {
        'title': title.strip(),
        'all_text': "\n".join(all_text),
    }

def main():
    try:
        url = "https://fr.wikipedia.org/wiki/Kylian_Mbapp%C3%A9" #on bouclera sur plusieurs fichiers
        data = scrape_page(url)
        with open('data.html', 'w') as extract_data:
            extract_data.write(f"Titre : {data['title']}\n\n")
            extract_data.write("Contenu de la page :\n")
            extract_data.write(data['all_text'])
        print(f"Le fichier sur {data['title']} a bien été scrapper et ajouter dans data.html")
    except Exception as e:
        return {'error': str(e)}

main()