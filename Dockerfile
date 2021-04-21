FROM python

ENV tg_token xxxxxx

COPY ./requirements.txt /
COPY ./chatbot.py /

RUN pip3 install -r requirements.txt
CMD python3 chatbot.py