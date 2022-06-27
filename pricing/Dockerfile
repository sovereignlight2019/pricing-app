FROM ubi8/python-36:latest

MAINTAINER scottryan@sovereignlight.solutions
ADD pricing .

RUN pip install flask && \
    pip install routes && \
    pip install psycopg2-binary && \
    pip install python-dotenv

expose 8001

ENV FLASK_APP=pricing
ENV FLASK_RUN_PORT=8001

CMD flask run -h 0.0.0.0 -p 8001