import requests
from bs4 import BeautifulSoup

r = requests.get("https://books.toscrape.com/index.html")
soup = BeautifulSoup(r.content, "html.parser")

print(soup)