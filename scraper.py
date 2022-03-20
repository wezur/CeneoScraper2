import requests
from bs4 import BeautifulSoup
from review import Review

request = requests.get('https://www.ceneo.pl/96092975#tab=reviews')

soup = BeautifulSoup(request.text, 'html.parser')

test = Review(soup.select('div.js_product-reviews')[0].select('div.js_product-review')[0])

print(test.pros)
# lista opinii - div.js_product-reviews
# opinia - div.js_product-review
# identyfikator opinii - div.js_product-review[data-entry-id]
# autor - span.user-post__author-name
# rekomendacja - span.user-post__author-recomendation > em
# liczba gwiazdek - span.user-post__score-count
# czy opinia jest potwierdzona zakupem
# data wystawienia opinii - user-post__published > time[datetime]:nth-child(1)
# data zakupu produktu - user-post__published > time[datetime]:nth-child(1)
# ile osób uznało opinię za przydatną 
# ile osób uznało opinię za nieprzydatną
# treść opinii
# lista wad
# lista zalet
