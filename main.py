import requests
import csv
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/1000-places-to-see-before-you-die_1/index.html"

# Requete pour obtenir le contenu de la page et la parser
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

# Fonction qui recupere les infos d'un livre et le stocke dans un dictionnaire
def get_book_info(soup):

    # Isoler les données qui nous interessent
    product_info = soup.find_all('td')
    UPC = product_info[0].text
    price_including_tax = product_info[2].text
    price_excluding_tax = product_info[3].text
    number_available = product_info[5].text
    title = soup.find('h1').text
    product_description = soup.find('p', class_=False).text
    image_url = soup.find('img')['src']
    nav = soup.find_all('a')
    category = nav[3].text
    stars = soup.find('p', class_='star-rating')
    review_rating = stars['class'][1]

    # Les infos d'un livre
    book_infos = {'product_page_url': url,
              'universal_ product_code (upc)': UPC,
              'title': title,
              'price_including_tax': price_including_tax,
              'price_excluding_tax': price_excluding_tax,
              'number_available': number_available,
              'product_description': product_description,
              'category': category,
              'review_rating': review_rating,
              'image_url': image_url
              }
    return book_infos

# Fonction qui charge les données en csv
def load_data(book_infos, bts):
    fieldnames = book_infos.keys() # Les clés du dictionnaire deviennent les en-tete
    with open(bts, mode='a', newline='', encoding='utf-8') as csvfile: # Filename, append mode, separation, cryptage
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader() # Ecriture des en-tete
        writer.writerow(book_infos) # Ecriture des datas

chemin = "/Users/guwoop/Documents/books_to_scrape/bts.csv"

book_infos = get_book_info(soup)
load_data(book_infos, chemin)
