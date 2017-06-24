FROM ubuntu:xenial
ADD . /code
WORKDIR /code
RUN apt-get update && apt-get install -y \
    python3.5 \
    python-pip \
    python-dev \
    build-essential
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "run.py"]
