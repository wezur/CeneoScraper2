from flask import Flask, render_template
from scraper import scrapProduct, scrapReviews

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', title="Strona główna")

@app.route('/extract/')
def extract():
    return render_template('extract.html', title="Ekstracja opinii")

@app.route('/product/list/')
def productList():
    reviews = [scrapReviews('113706425'), scrapReviews('104791205')]
    products = [scrapProduct('113706425', reviews[0]), scrapProduct('104791205', reviews[1])]
    return render_template('list.html', products=products)

@app.route('/product/<productId>/')
def product(productId):
    reviews = scrapReviews(productId)
    product = scrapProduct(productId, reviews)
    return render_template('product.html', reviews=reviews, product=product, title=f'Opinie produktu - {product.name}')