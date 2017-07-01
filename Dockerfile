FROM python:3.4-slim

ADD . /code
WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python-dev

RUN pip install -r requirements.txt
CMD ["python", "run.py"]
