import os
from flask import request
import requests
from models import *
import logging
from flask import Response

BASEDIR = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(level=logging.WARNING,
                    filename=os.path.join(BASEDIR, 'app.log'),
                    format="%(asctime)s %(levelname)s %(message)s")




with app.app_context():
    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/promo/<string:target>/')
    def promo_id(target):
        return render_template('index.html')
    
    
    @app.route('/product/<string:target>/')
    def product_id(target):
        return render_template('index.html')
    
    
    @app.route('/api/promo/<string:target>/')
    def promo_id_api(target):
        print(Main.query.filter(Main.link.like(f"%promo/{target}%")))
        return jsonify(serializer(Main.query.filter(Main.link.like(f"%promo/{target}%")).all()))


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


    @app.route('/robots.txt')
    def robots_txt():
        return Response("User-agent: *\nAllow: *", mimetype='text/plain')


    @app.route('/<string:id>/')
    def other(id):
        return render_template('index.html')
    

    def serializer(data):
        try:
            if not data:
                return []
            
            if isinstance(data, (bool, str, int, float, type(None))):
                return data

            if isinstance(data, list):
                result = []
                for item in data:
                    result.append(serializer(item))

                return result

            try:
                return {key: value for key, value in data.__dict__.items() if not key.startswith('_')}
            except:
                result = {}
                for key, value in data._asdict().items():
                    if not isinstance(value, (bool, str, int, float, type(None))):
                        result.update(serializer(value))
                    else:
                        result.update({key: value})
                return result

        except Exception as e:
            logging.error(e)
            return []


    def compileData(rows):
        compiled_rows = []
        for row in rows:
            current_row = next((item for item in compiled_rows if row['id'] == item['id']), None)
            if current_row is None:
                image = [row['image_name']] if row['image_name'] is not None else []
                row.update({'carousel': image})
                row.pop('image_name')
                compiled_rows.append(row)
            else:
                if row['image_name'] is not None:
                    current_row['carousel'].append(row['image_name'])
        return compiled_rows



if __name__ == "__main__":
    app.run(debug=True)