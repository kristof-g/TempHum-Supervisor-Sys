# PYTHON BASE IMAGE FOR BACKEND
FROM python:3

RUN apt-get update
RUN apt-get -y install curl
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get -y install nodejs

WORKDIR /home
ENV PYTHONPATH=/home

COPY server ./server
COPY front ./front
COPY builder ./builder
COPY run.py ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /home/front
CMD [ "npm", "install" ]
WORKDIR /home
CMD [ "python", "./builder/build.py PROD" ]
EXPOSE 3125
ENTRYPOINT [ "python", "./run.py" ]
#ENTRYPOINT /bin/bash
