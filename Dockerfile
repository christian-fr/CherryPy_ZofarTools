FROM python:3.6-alpine3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
RUN \
 apk add --update --no-cache \
           graphviz \
           ttf-freefont && \
 pip install --no-cache-dir pipenv && \
 apk --purge del .build-deps
 
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system

# Copy project
COPY . /code/

