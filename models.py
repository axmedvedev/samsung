from flask import Flask, render_template, url_for, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)

CORS(app, origins=[
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5000",
    "http://localhost:8080",
    "http://localhost:5000",
])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Main(db.Model):
    __tablename__ = 'main'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Integer)
    button = db.Column(db.Integer)
    link = db.Column(db.String(255))
    home_image = db.Column(db.String(255))
    promo_image = db.Column(db.String(255))
    group = db.Column(db.Integer)
    sort = db.Column(db.Integer)
    date_start = db.Column(db.String(10))
    date_end = db.Column(db.String(10))
    home_sort = db.Column(db.Integer)
    home_status = db.Column(db.Integer)
    size = db.Column(db.Integer)
    name = db.Column(db.String(255))
    htmlFile = db.Column(db.String(255))
    description = db.Column(db.Text())
    content = db.Column(db.Text())
    images = db.relationship('PromoImage', back_populates='main', lazy='dynamic')
    slider_status = db.Column(db.Integer)

    def __repr__(self) -> str:
        return self.name


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Integer)
    link = db.Column(db.String(255))
    desktop_image = db.Column(db.String(255))
    mobile_image = db.Column(db.String(255))
    kaspi = db.Column(db.String(255))
    name = db.Column(db.String(255))
    meta_description = db.Column(db.String(255))
    content = db.Column(db.Text())
    images = db.relationship('ProductImage', back_populates='product', lazy='dynamic')

    def __repr__(self) -> str:
        return self.name


class ProductImage(db.Model):
    __tablename__ = 'product_image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    image = db.Column(db.String(255))
    product = db.relationship('Product', back_populates='images')

    def __repr__(self) -> str:
        return self.image


class Carousel(db.Model):
    __tablename__ = 'carousel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slide = db.Column(db.String(255))
    alt = db.Column(db.String(255))
    link = db.Column(db.String(255))
    sort = db.Column(db.Integer)
    status = db.Column(db.Integer)

    def __repr__(self) -> str:
        return self.alt


class Slider(db.Model):
    __tablename__ = 'slider'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slide = db.Column(db.String(255))
    slide_m = db.Column(db.String(255))
    alt = db.Column(db.String(255))
    link = db.Column(db.String(255))
    sort = db.Column(db.Integer)
    status = db.Column(db.Integer)

    def __repr__(self) -> str:
        return self.alt


class PromoImage(db.Model):
    __tablename__ = 'promo_image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    main_id = db.Column(db.Integer, db.ForeignKey('main.id'))
    image = db.Column(db.String(255))
    main = db.relationship('Main', back_populates='images')

    def __repr__(self) -> str:
        return self.image