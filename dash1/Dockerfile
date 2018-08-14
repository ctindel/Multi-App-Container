FROM python:3.6.2

RUN mkdir -p /home/project/dash1
WORKDIR /home/project/dash1
COPY requirements.txt /home/project/dash1
RUN pip install --upgrade pip --no-cache-dir -r requirements.txt

COPY . /home/project/dash1

