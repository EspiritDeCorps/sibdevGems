FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /gems
WORKDIR /gems
COPY requirements.txt /gems/
RUN pip install -r requirements.txt
COPY . /gems/
