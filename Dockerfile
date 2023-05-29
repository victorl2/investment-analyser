FROM python:3.9.10

RUN apt-get update && \
    apt-get install --no-install-recommends -y

RUN mkdir -p /usr/src/app/src
WORKDIR /usr/src/app

# install requirements
COPY ./requirements.txt /usr/src/app/

# copy .env file
COPY ./.env /usr/src/app/

RUN python3 -m pip install --no-cache-dir -r requirements.txt

# move codebase over
COPY ./src /usr/src/app/src

# run the application
CMD ["/usr/local/bin/python3", "/usr/src/app/src/main.py"]