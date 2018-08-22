FROM python:3.6.2

RUN mkdir -p /home/project/dash2
WORKDIR /home/project/dash2
COPY requirements.txt /home/project/dash2
RUN pip install --upgrade pip --no-cache-dir -r requirements.txt

COPY . /home/project/dash2

