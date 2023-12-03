import requests
from bs4 import BeautifulSoup
import csv

def get_all_category():
    category_urls = []
    home_url = "http://books.toscrape.com/index.html"
    r = requests.get(home_url)
    soup = BeautifulSoup(r.content, "html.parser")
    ul_s = soup.find_all('ul')
    for ul in ul_s:
        li_s = ul.find_all('li')
        for li in li_s:
            a_tag = li.find('a')
            if a_tag:
                link = f"http://books.toscrape.com/{li.find('a')['href']}"
                print(link)
                if link not in category_urls:
                    category_urls.append(link)
                else:
                    continue
    del(category_urls[0:2])
    del(category_urls[-1])
    return category_urls

def get_all_books(category_url):
    book_list = []
    r = requests.get(category_url)
    soup = BeautifulSoup(r.content, "html.parser")
    urls_cut = soup.find_all('h3')
    for url in urls_cut:
        link = f"http://books.toscrape.com/catalogue/{url.find('a')['href'].strip('../../..')}"
        book_list.append(link)
    return book_list

def get_book_info(link):
    # Extract
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    product_info = soup.find_all('td')
    UPC = product_info[0].text
    price_including_tax = product_info[2].text
    price_excluding_tax = product_info[3].text
    number_available = product_info[5].text
    title = soup.find('h1').text
    product_description = soup.find('meta', {'name': 'description'})['content']
    image_url = soup.find('img')['src']
    nav = soup.find_all('a')
    category = nav[3].text
    stars = soup.find('p', class_='star-rating')
    review_rating = stars['class'][1]

    # Les infos d'un livre
    book_infos = {
        'product_page_url': link,
        'universal_product_code (upc)': UPC,
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

def load_data(book_infos, category, bts):
    fieldnames = book_infos[0].keys()
    with open(f'{category}_{bts}', mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        writer.writerows(book_infos)

# Variables
all_category_urls = get_all_category()

# Lancement
for category_url in all_category_urls:
    book_list = get_all_books(category_url)
    all_books_info = []

    for book_link in book_list:
        book_info = get_book_info(book_link)
        all_books_info.append(book_info)

    load_data(all_books_info, category_url.split('/')[-3], 'books_data.csv')

print("All categories processed.")
