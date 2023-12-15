from flask import Flask, render_template, url_for
from flask import request
import requests
from flask_cors import CORS
from flask.json import jsonify
from static.config import version

app = Flask(__name__)
CORS(app, origins=[
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5000",
    "http://localhost:8080",
    "http://localhost:5000",
])
    

with app.app_context():

    @app.route('/version')
    def get_version():
        return jsonify(v=version)

    @app.route('/')
    def index():
        return render_template('index.html')
    

    @app.route('/<string:id>/')
    def other(id):
        return render_template('index.html')
    
    @app.route('/promo/')
    def promo():
        return render_template('index.html')
    
    @app.route('/promo/<string:id>/')
    def promo_id(id):
        return render_template('index.html')
    
    @app.route('/product/<string:id>/')
    def product_id(id):
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




if __name__ == "__main__":
    app.run(debug=True)