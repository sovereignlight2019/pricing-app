FROM ubi8/python-36:latest

MAINTAINER scottryan@sovereignlight.solutions
ADD pricing .

RUN pip install flask && \
    pip install routes && \
    pip install psycopg2-binary && \
    pip install python-dotenv && \
    pip install config && \
    pip instal flask-wtf

expose 8000

ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_PORT=8000

CMD flask run -h 0.0.0.0 -p 8000