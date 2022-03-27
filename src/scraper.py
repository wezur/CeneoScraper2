import requests
from bs4 import BeautifulSoup
from review import Review
from product import Product

def scrapReviews(productID):
	hasNextPage = True
	pageNumber = 1

	reviewList = []
	while(hasNextPage):
		request = requests.get(f'https://www.ceneo.pl/{productID}/opinie-{pageNumber}')
		soup = BeautifulSoup(request.text, 'html.parser')

		reviewListHtml = soup.select('div.js_product-reviews')[0].select('div.js_product-review')
		for reviewEle in reviewListHtml:
			reviewList.append(Review(reviewEle))
		if len(soup.select('a.pagination__next')) > 0:
			pageNumber += 1
		else:
			hasNextPage = False
	return reviewList

def scrapProduct(productID, reviews):
	request = requests.get(f'https://www.ceneo.pl/{productID}')
	soup = BeautifulSoup(request.text, 'html.parser')
	product = Product(productID, soup, f'https://www.ceneo.pl/{productID}', reviews)
	return product