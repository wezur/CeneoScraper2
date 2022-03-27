import jsonpickle
from flask import Flask, render_template, send_file
from scraper import scrapProduct, scrapReviews
import matplotlib.pyplot as plt
import json
import csv
import os

import base64
from io import BytesIO
import pandas as pd
from matplotlib.figure import Figure
from types import SimpleNamespace

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', title="Strona główna")

@app.route('/extract/')
def extract():
    return render_template('extract.html', title="Ekstracja opinii")

@app.route('/product/list/')
def productList():
    file_list = os.listdir('./static/cache/products')
    data = []
    for file in file_list:
        with open(f'./static/cache/products/{file}', 'r') as file_data:
            data.append(json.load(file_data))
    # reviews = [scrapReviews('113706425'), scrapReviews('104791205')]
    # products = [scrapProduct('113706425', reviews[0]), scrapProduct('104791205', reviews[1])]
    return render_template('list.html', products=data, title="Lista zapisanych produktów")

@app.route('/product/<productId>/download/<type>/')
def download(productId, type):
    if type=='json':
        return send_file(f'./static/cache/reviews/{productId}.json')
    elif type=='csv':
        with open(f'./static/cache/reviews/{productId}.json') as json_file:
            df = pd.read_json(json_file)
        df.to_csv(f'./static/cache/reviews/{productId}.csv', encoding='utf-8', index=False)
        return send_file(f'./static/cache/reviews/{productId}.csv')
    elif type=='xlsx':
        with open(f'./static/cache/reviews/{productId}.json') as json_file:
            df = pd.read_json(json_file)
        df.to_excel(f'./static/cache/reviews/{productId}.xlsx', encoding='utf-8', index=False)
        return send_file(f'./static/cache/reviews/{productId}.xlsx')

@app.route('/product/<productId>/graphs/')
def graphs(productId):
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
    with open(f'./static/cache/reviews/{productId}.json', 'r') as file:
        recommendationData = {
            'Polecam': 0,
            'Nie polecam': 0,
            'Brak': 0
        }
        starCountData = {
            '5': 0,
            '4,5': 0,
            '4': 0,
            '3,5': 0,
            '3': 0,
            '2,5': 0,
            '2': 0,
            '1,5': 0,
            '1': 0,
            '0,5': 0
        }
        data = json.load(file)
        for review in data:
            if review['recommendation'] == 'Polecam':
                recommendationData['Polecam'] += 1
            elif review['recommendation'] == 'Nie polecam':
                recommendationData['Nie polecam'] += 1
            else:
                recommendationData['Brak'] += 1
            starCountData[review['starCount'].split('/')[0]] += 1

    plt.switch_backend('Agg') 
    labels1 = recommendationData.keys()
    sizes1 = recommendationData.values()
    labels1 = [f'{l}, {s/len(data)*100:0.1f}%' for l, s in zip(labels1, sizes1)]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes1,
            shadow=True, startangle=90)
    fig1.legend(labels1, loc='lower left', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)
    plt.title('Udział poszczególnych rekomendacji w ogólnej liczbie opinii')
    buf1 = BytesIO()
    fig1.savefig(buf1, format="png", bbox_inches='tight')

    data1 = base64.b64encode(buf1.getbuffer()).decode("ascii")

    labels2 = starCountData.keys()
    sizes2 = starCountData.values()
    fig2, ax2 = plt.subplots()
    ax2.bar(labels2, sizes2)
    plt.title('Liczba opinii z poszczególnymi liczbami gwiazdek')
    buf2 = BytesIO()
    fig2.savefig(buf2, format="png")

    data2 = base64.b64encode(buf2.getbuffer()).decode("ascii")

    return render_template('graphs.html', graph1=data1, graph2=data2, title='Wykresy')

@app.route('/product/<productId>/')
def product(productId):
    try:
        reviews = scrapReviews(productId)
        with open(f'./static/cache/reviews/{productId}.json', 'w') as file:
            jsonpickle.set_encoder_options('json', indent=2, ensure_ascii=False)
            file.write(jsonpickle.encode(reviews))
        product = scrapProduct(productId, reviews)
        with open(f'./static/cache/products/{productId}.json', 'w') as file:
            jsonpickle.set_encoder_options('json', indent=2, ensure_ascii=False)
            file.write(jsonpickle.encode(product))
        return render_template('product.html', reviews=reviews, product=product, title=f'Opinie produktu - {product.name}')
    except Exception as e:
        return render_template('extract.html', error=e, title="Ekstracja opinii")

@app.route('/about/')
def about():
    return render_template('about.html', title="O autorze")