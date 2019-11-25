# Set up Python3.6
FROM python:3.6
ENV LOGPATH /var/log
RUN mkdir -p /app
ADD ./ /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# Install MongoDB
# https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
#RUN apt-get install gnupg
#RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
#RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list
#RUN mkdir -p /data/db
#RUN apt-get update && apt-get install -y mongodb-org
#RUN mkdir -p /var/log
#RUN apt-get install -y systemd
##RUN systemctl unmask mongod
##RUN service mongod start
#RUN mongod &
#RUN cat /var/log/mongodb.log

# Install MongoDB
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" |  tee /etc/apt/sources.list.d/mongodb-org-4.0.list
RUN apt-get update \
 && apt-get install -y mongodb-org \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /data/db
RUN mkdir -p /var/log
RUN mongod --fork --logpath=/var/log/mongodb.log
RUN mongod --fork --logpath=/var/log/mongodb.log
RUN cat /var/log/mongodb.log

#RUN mongo

# Start app
EXPOSE 5000
EXPOSE 80

#RUN python3 data_acquire.py & python3 app.py

