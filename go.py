
def get_all_category():
    final = []
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
                if link not in final:
                    final.append(link)
                else:
                    continue
    del(final[0:2])
    del(final[-1])
    return final

def get_page_2(final):
    for link in final:
        r = requests.get(link)
        soup = BeautifulSoup(r.content, "html.parser")
        next_page = soup.find('li', class_='next')
        if next_page:
            link = link[:-10]
            next_page_link = f"{link}{next_page.find('a')['href']}"
            if next_page_link not in final:
                final.append(next_page_link)
                for next_page_link in final:
                    next_next_pages = soup.find('li', class_='next')
                    if next_next_pages:
                        next_next_pages_link = f"{link}{next_next_pages.find('a')['href']}"
                        print(next_next_pages_link)
                        if next_next_pages_link not in final:
                            final.append(next_next_pages_link)
                        else:
                                break
            else:
                    break
    return final

# Usage
final_list = get_all_category()
category_list = get_page_2(final_list)
print(category_list)
