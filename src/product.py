class Product:
	def __init__(self, productHtml, link, reviews):
		self.name = productHtml.select('h1.product-top__product-info__name')[0].text
		self.image = productHtml.select('div.product-top__image-carousel__current > a > img[src]')[0]['src']
		self.link = link
		self.reviewsCount = len(reviews)
		self.prosCount = 0
		self.consCount = 0
		self.averageStarCount = 0
		for review in reviews:
			self.prosCount += len(review.pros)
			self.consCount += len(review.cons)
			self.averageStarCount += int(review.starCount[0])
		self.averageStarCount = round(self.averageStarCount / len(reviews), 2)