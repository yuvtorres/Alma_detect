FROM python:3.8-slim

ADD ./ ./

RUN pip3 install -r requirements.txt
RUN python -m nltk.downloader vader_lexicon
CMD ["python3","-u", "api.py"]
