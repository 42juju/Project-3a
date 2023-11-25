# an offical python immage as base image
FROM python:3.8-slim-buster
# set the working directory in the container in the /app
WORKDIR /app
#copy the contents from the current directory in to the container at /app
COPY . /app 
# upgrade pip 
RUN pip install --upgrade pip 
#intall any needed packages 
RUN pip install --no-cache-dir -r requirements.txt
#set default commnand 
CMD [ "python", "flaskapp.py" ]