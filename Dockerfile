FROM alpine:edge

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
RUN \
 apk add --update --no-cache  \
           graphviz \
           ttf-freefont \
	   python3 \
	   py3-lxml \
	   py3-graphviz \
	   py3-pygraphviz \
	   py3-cryptography
#	   && \
# pip install --no-cache-dir pipenv

#COPY Pipfile Pipfile.lock /code/
#RUN pipenv install --system

# Copy project
COPY . /code/

