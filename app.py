from flask import Response, render_template, url_for, jsonify, request
from mongo import MongoDB
import requests
from models import *
from utils import *

with app.app_context():
    #base routing
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/promo/<string:target>/')
    def promo_id(target):
        return render_template('index.html')

    @app.route('/product/<string:target>/')
    def product_id(target):
        return render_template('index.html')

    @app.route('/robots.txt')
    def robots_txt():
        return Response("User-agent: *\nAllow: *", mimetype='text/plain')

    @app.route('/<string:id>/')
    def other(id):
        return render_template('index.html')

    @app.route('/care-service/', methods=['GET','POST'])
    def care_service():
        try:
            if request.method == 'POST':
                request_data = request.get_json()
                message = f"Имя: {request_data['name']}\nТелефон: {request_data['phone']}\nСообщение: {request_data['message']}"
                token_bot = '6551926073:AAEi8rDWlAMYv_tQLjSQXC6nrvkbBvn4YIo'
                query_string = (
                    f'&chat_id=-4036517228'
                    f'&text={message}'
                    f'&parse_mode=HTML'
                    f'&disable_web_page_preview=True'
                )
                requests.get(f"https://api.telegram.org/bot{token_bot}/sendMessage?{query_string}")
                return b'{"status": "ok"}'
            else:
                return render_template('index.html')
        except Exception as e:
            return f'{{"status": "error", "message": "{e}"}}'



    #from Alchemy
    @app.route('/api/slider/')
    def sliders():
        return jsonify(serializer(Slider.query.all()))

    @app.route('/api/carousel/')
    def carousel():
        return jsonify(serializer(Carousel.query.all()))

    @app.route('/api/main/')
    def main():
        return jsonify(compileData(serializer(Main.query
                                              .join(PromoImage, Main.images, isouter=True)
                                              .add_columns(PromoImage.image.label("image_name"))
                                              .all())))

    @app.route('/api/product/')
    def product():
        return jsonify(compileData(serializer(Product.query
                                              .join(ProductImage, Product.images)
                                              .add_columns(ProductImage.image.label("image_name"))
                                              .all())))

    @app.route('/api/promo/<string:target>/')
    def promo_id_api(target):
        return jsonify(compileData(serializer(Main.query
                                  .join(PromoImage, Main.images, isouter=True)
                                  .add_columns(PromoImage.image.label("image_name"))
                                  .filter(Main.link.like(f"%promo/{target}%")).all())))


    #from MONGO
    @app.route('/api/v2/main/')
    def api_main():
        db = MongoDB(collection='main', config=Config.MONGO)
        data = list(db.get_all())
        return jsonify(data)
    
    @app.route('/api/v2/promo/<string:target>/')
    def api_main_detail(target):
        db = MongoDB(collection='main', config=Config.MONGO)
        data = db.get_one('link', f"promo/{target}")
        return jsonify(data)
    
    @app.route('/api/v2/product/')
    def api_product():
        db = MongoDB(collection='product', config=Config.MONGO)
        data = list(db.get_all())
        return jsonify(data)
    
    @app.route('/api/v2/carousel/')
    def api_carousel():
        db = MongoDB(collection='carousel', config=Config.MONGO)
        data = list(db.get_all())
        return jsonify(data)
    
    @app.route('/api/v2/slider/')
    def api_slider():
        db = MongoDB(collection='slider', config=Config.MONGO)
        data = list(db.get_all())
        return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)