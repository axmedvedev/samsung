FROM python:3.10.11

WORKDIR /

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /static_temp

COPY /static/. /static_temp/

COPY . .

CMD sh -c "cp -R /static_temp/* /static/ && rm -r /static_temp/ && gunicorn -b 0.0.0.0:5000 app:app"