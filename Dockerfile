FROM python:3

# Set env variables
RUN apt-get update
RUN apt-get install -y --no-install-recommends gdal-bin
RUN apt-get install -y mime-support
WORKDIR /code

ENV PYTHONUNBUFFERED 1

# Set volume for database and static files.
RUN mkdir -p /static /media

# Install requirements
COPY requirements.txt /code/requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install Pillow psycopg2

# Copy source code
COPY . /code
COPY ./docker-entrypoint.sh ./docker-entrypoint.sh

# Set docker-entrypoint
RUN chmod +x /code/docker-entrypoint.sh
CMD ["/code/docker-entrypoint.sh"]
