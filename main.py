import requests
from bs4 import BeautifulSoup
import csv
import os
import urllib.request

#Extraction des URL Catégory
def get_all_category_urls():
    category_urls = []
    home_url = "http://books.toscrape.com/index.html"
    response = requests.get(home_url)
    soup = BeautifulSoup(response.content, "html.parser")

    for ul in soup.find_all('ul'):
        for li in ul.find_all('li'):
            a_tag = li.find('a')
            if a_tag:
                link = f"http://books.toscrape.com/{a_tag['href']}" #Reconstruction du lien complet
                if link not in category_urls:
                    category_urls.append(link)

    #Suppression des liens inutiles
    del category_urls[0:2]
    del category_urls[-1]

    return category_urls

#Extraction des URL Catégory des pages "Next"
def get_page_urls(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, "html.parser")
    next_page = soup.find('li', class_='current')

    if next_page:
        page_number = int(next_page.get_text(strip=True)[-1])#Si il y a "next page" et combien
        base_url = category_url.rsplit('/', 1)[0]

        page_urls = [f"{base_url}/page-{i}.html" for i in range(1, page_number + 1)]#Reconstitution du lien complet
        return page_urls

    return [category_url]

#Extraction des URL Book
def get_all_books_urls(page_url):
    book_urls = []
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")
    urls_cut = soup.find_all('h3')

    for url in urls_cut:
        link = f"http://books.toscrape.com/catalogue/{url.find('a')['href'].strip('../../..')}"#Reconstitution du lien complet
        if link not in book_urls:
            book_urls.append(link)

    return book_urls

def download_img(dl_img_link, title, category):
    print(f"{dl_img_link=} ")
    print(f"{title=}")
    print(f"{category=}")
    urllib.request.urlretrieve(dl_img_link, f"datas/{category}/{title}.png")

#Extraction de Book Infos
def get_book_info(link, category_folder):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    product_info = soup.find_all('td')
    UPC = product_info[0].text
    price_including_tax = product_info[2].text
    price_excluding_tax = product_info[3].text
    number_available = product_info[5].text
    title = soup.find('h1').text
    image_url = soup.find('img')['src']
    dl_img_link = f"http://books.toscrape.com/{image_url.strip('../../..')}"
    nav = soup.find_all('a')
    category = nav[3].text
    stars = soup.find('p', class_='star-rating')
    review_rating = stars['class'][1]
    #Exception car certain n'ont pas de description
    try:
        product_description = soup.find('p', class_=False).text
    except (AttributeError, TypeError):
        product_description = None

#Données Book
#Keys: Raw
    book_info = {
        'title': title,
        'product_page_url': link,
        'universal_product_code (upc)': UPC,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'product_description': product_description,
        'category': category,
        'review_rating': review_rating,
        'image_url': dl_img_link
    }
    title = title.replace("/", " ")# Probleme lors de l'ecriture des images lié au nom
    download_img(dl_img_link, title, category_folder)# Appel de la fonction image
 
    return book_info

#Ecriture en données CSV
def write_to_csv(book_infos, category):
    fieldnames = book_infos[0].keys()
    category_filename = f'datas/{category}/data.csv'

    with open(category_filename, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(book_infos)

# Appel des fonctions
all_category_urls = get_all_category_urls()
os.mkdir("datas")
for category_url in all_category_urls:
    page_urls = get_page_urls(category_url)
    category = category_url.split('/')[-2] 
    
    os.mkdir(f"datas/{category}")

    for page_url in page_urls:
        book_urls = get_all_books_urls(page_url)
        all_books_info = []

        for book_url in book_urls:
            book_info = get_book_info(book_url, category)
            all_books_info.append(book_info)
    

    write_to_csv(all_books_info, category)
