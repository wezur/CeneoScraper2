from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', title="Strona główna")

@app.route('/extract/')
def extract():
    return render_template('extract.html', title="Ekstracja opinii")

@app.route('/product/<productId>/')
def product(productId):
    return render_template('product.html')