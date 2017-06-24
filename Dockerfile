FROM ubuntu:xenial
ADD . /code
WORKDIR /code
RUN apt-get -y install \
    python3.5 \
    python-pip \
    python-dev \
    build-essential \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg8-dev \
    zlib1g-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "run.py"]
