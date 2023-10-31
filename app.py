from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request
import requests

app = Flask(__name__)
    

with app.app_context():
    @app.route('/')
    def index():
        return render_template('index.html')
    

    @app.route('/<int:id>')
    def other():
        return render_template('index.html')
    
    @app.route('/care-service', methods=['POST'])
    def care_service():
        try:
            if request.method == 'POST':
                request_data = request.get_json()
                message = f"Имя: {request_data['name']}\nТелефон: {request_data['phone']}\nСообщение: {request_data['message']}"
                token_bot = '6551926073:AAEi8rDWlAMYv_tQLjSQXC6nrvkbBvn4YIo'
                query_string = (
                    f'&chat_id=-963225760'
                    f'&text={message}'
                    f'&parse_mode=HTML'
                    f'&disable_web_page_preview=True'
                )
                requests.get(f"https://api.telegram.org/bot{token_bot}/sendMessage?{query_string}")
            return b'{"status": "ok"}'
        except Exception as e:
            return b'{"status": "error"}'




if __name__ == "__main__":
    app.run(debug=True)