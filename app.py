import os
import shopify
import binascii
import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  email = db.Column(db.String(100))

  def __init__(self, name, email):
    self.name = name
    self.email = email


@app.route('/', methods=['GET'])
def index():
  return render_template('index.html', users=User.query.all())


@app.route('/user', methods=['POST'])
def user():
  u = User(request.form['name'], request.form['email'])
  db.session.add(u)
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/userNew', methods=['POST'])
def userNew():
  u = User(request.form['name'], request.form['email'])
  db.session.add(u)
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/accessToken', methods=['POST'])
def accessToken():
  API_KEY = '0072294b270c3a24e9a9dfda9bf0fc31'
  API_SECRET = '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'
  shopify.Session.setup(api_key=API_KEY, secret=API_SECRET)

  shop_url = "9xworks.myshopify.com"
  api_version = '2020-10'
  access_token = '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'
  session = shopify.Session(shop_url, api_version, access_token)
  shopify.ShopifyResource.activate_session(session)

  shop = shopify.Shop.current() # Get the current shop
  #product = shopify.Product.find(179761209) # Get a specific product
  print(shop)
  # execute a graphQL call
  return shopify.GraphQL().execute("{ shop { name id } }")


  print(res)
if __name__ == '__main__':
  db.create_all()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
