# Set up Python3.6
FROM mongo
RUN apt-get update
RUN apt-get install -y python3.6 curl python3-venv python3-pip
RUN alias python3=python3.6

# Setup directory
RUN mkdir -p /app
ADD ./ /app
WORKDIR /app

# Start app
EXPOSE 5000
EXPOSE 80
#RUN pip3 install pymongo
#RUN python3 -c 'import pymongo;list(pymongo.MongoClient().get_database("energy").energy.find())'
RUN pip3 install -r requirements.txt
RUN python3 data_acquire.py # & python3 app.py

