# Set up MongoDB and Python3.6
FROM mongo
RUN mkdir -p /var/log
#RUN mongod --fork --logpath /var/log/mongodb.log

RUN apt-get update
RUN apt-get install -y python3.6 curl python3-venv python3-pip
RUN alias python3=python3.6

# Setup directory
RUN mkdir -p /app
COPY ./ /app
WORKDIR /app

# Start app
EXPOSE 5000
EXPOSE 80
RUN pip3 install -r requirements.txt
CMD sh start.sh

