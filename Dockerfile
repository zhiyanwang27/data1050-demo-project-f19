# Set up Python3.6
FROM python:3.6
ENV LOGPATH /var/log
RUN mkdir -p /app
ADD ./ /app
WORKDIR /app

# Install MongoDB
# https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
RUN apt-get install gnupg
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list
RUN mkdir -p /data/db
RUN apt-get update && apt-get install -y mongodb-org
RUN mongod --fork --logpath /var/log/mongodb.log

# Start app
EXPOSE 5000
EXPOSE 80


RUN pip3 install -r requirements.txt
RUN python3 data_acquire.py & python3 app.py

