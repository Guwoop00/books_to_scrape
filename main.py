import requests
from bs4 import BeautifulSoup

r = requests.get("http://books.toscrape.com/catalogue/1000-places-to-see-before-you-die_1/index.html")
soup = BeautifulSoup(r.content, "html.parser")

print(soup)