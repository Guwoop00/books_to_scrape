import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/1000-places-to-see-before-you-die_1/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

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
print(url)
print(UPC)
print(title)
print(price_including_tax)
print(price_excluding_tax)
print(number_available)
print(product_description)
print(category)
print(review_rating)
print(image_url)












titres = ['Product page', 'upc', 'title', 'price including tax', 'price excluding tax', 'number vailable', 'product description', 'category', 'review rating', 'image url' ]
description = [product_description, UPC, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url ]

en_tete = [titres, description]
print(en_tete)