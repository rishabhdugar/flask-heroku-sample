import os
import shopify
import binascii
import os

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')
API_KEY = '0072294b270c3a24e9a9dfda9bf0fc31'
API_SECRET = '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'
API_VERSION = '2020-10'

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
  shopify.Session.setup(api_key=API_KEY, secret=API_SECRET)

  session = shopify.Session(shop_url, api_version)
  request_params = {"code": request.form['code'], 
  "hmac": request.form['hmac'], 
  "host":request.form['host'],
  "shop":request.form['shop_url'],
  "state":request.form['state'],
  "timestamp": request.form['timestamp']};
  access_token = session.request_token(request_params) # request_token will validate hmac and timing attacks
  print(access_token)
  return jsonify(
        access_token=access_token,
        status="200"
  )

@app.route('/products', methods=['POST'])
def products():
  API_KEY = '0072294b270c3a24e9a9dfda9bf0fc31'
  API_SECRET = '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'
  shopify.Session.setup(api_key=API_KEY, secret=API_SECRET)

  shop_url = "9xworks.myshopify.com"
  api_version = '2020-10'
  access_token = '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'
  session = shopify.Session(shop_url, api_version, access_token)
  shopify.ShopifyResource.activate_session(session)

#{"code": "9f20acba867fab88f9425cf7e9e6bc91", 
#"hmac": "083a396b15e0018ea0e0f3eb7d32510a3ff4fc3faae6d8c8c3c5743bc98d6d03", 
#"host":"OXh3b3Jrcy5teXNob3BpZnkuY29tL2FkbWlu",
#"shop":"9xworks.myshopify.com",
#"state":"91519aa793a1a9ff05163c9cf51e01",
#"timestamp": "1641618459"}

  shop = shopify.Shop.current() # Get the current shop
  #products = shopify.Product.find(limit=50, page=1)
  #product = shopify.Product.find(179761209) # Get a specific product
  # execute a graphQL call
  u = User('shop', 'shopresp')
  print(shop)
  products = shopify.GraphQL().execute("{products (first: 3) {edges {node {id title } } } }")
  print(products)
  return redirect(url_for('index'))

@app.route('/loginUrl', methods=['POST'])
def loginUrl():
  shopify.Session.setup(api_key=API_KEY, secret=API_SECRET)

  shop_url = request.form['shop_url']
  state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
  redirect_uri = request.form['redirect_uri']
  scopes = ['read_products', 'read_orders']

  newSession = shopify.Session(shop_url, API_VERSION)
  auth_url = newSession.create_permission_url(scopes, redirect_uri, state)
  # redirect to auth_url
  return jsonify(
        auth_url=auth_url
  )


if __name__ == '__main__':
  db.create_all()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
