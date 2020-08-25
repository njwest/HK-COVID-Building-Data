FROM python:3.8-alpine

COPY ./ /

RUN pip install requirements.txt

CMD [ "python3", "./retrieve_data.py" ]
