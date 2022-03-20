class Review:
	def __init__(self, reviewHtml):
		self.reviewId = reviewHtml['data-entry-id']
		self.author = reviewHtml.select('span.user-post__author-name')[0].text
		self.recommendation = reviewHtml.select('span.user-post__author-recomendation > em')[0].text if len(reviewHtml.select('span.user-post__author-recomendation > em')) > 0 else None
		self.starCount = reviewHtml.select('span.user-post__score-count')[0].text if len(reviewHtml.select('span.user-post__score-count')) > 0 else None
		self.reviewDate = reviewHtml.select('span.user-post__published > time[datetime]:nth-child(1)')[0]['datetime'] if len(reviewHtml.select('span.user-post__published > time[datetime]:nth-child(1)')) > 0 else None
		self.purchaseDate = reviewHtml.select('span.user-post__published > time[datetime]:nth-child(2)')[0]['datetime'] if len(reviewHtml.select('span.user-post__published > time[datetime]:nth-child(2)')) > 0 else None
		self.voteYesCount = reviewHtml.select('span[id^=votes-yes]')[0].text
		self.voteNoCount = reviewHtml.select('span[id^=votes-no]')[0].text
		self.content = reviewHtml.select('div.user-post__text')[0].text	if len(reviewHtml.select('div.user-post__text')) > 0 else None
		pros = reviewHtml.select('div.review-feature__col:has( > div.review-feature__title--positives)')
		cons = reviewHtml.select('div.review-feature__col:has( > div.review-feature__title--negatives)')
		self.pros = []
		self.cons = []
		if len(pros) > 0:
			for prosEle in pros[0].select('div.review-feature__item'):
				self.pros.append(prosEle.text)
		if len(cons) > 0:
			for consEle in cons[0].select('div.review-feature__item'):
				self.cons.append(consEle.text)