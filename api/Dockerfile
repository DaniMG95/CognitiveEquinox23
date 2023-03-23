FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

RUN python3 -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

#
COPY ./app /code/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
