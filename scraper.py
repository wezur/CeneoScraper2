import requests
from bs4 import BeautifulSoup
from review import Review

hasNextPage = True
pageNumber = 1

reviewList = []
while(hasNextPage):
	request = requests.get(f'https://www.ceneo.pl/96092975/opinie-{pageNumber}')
	soup = BeautifulSoup(request.text, 'html.parser')

	reviewListHtml = soup.select('div.js_product-reviews')[0].select('div.js_product-review')
	for reviewEle in reviewListHtml:
		reviewList.append(Review(reviewEle))
	if len(soup.select('a.pagination__next')) > 0:
		pageNumber += 1
	else:
		hasNextPage = False

print(reviewList)