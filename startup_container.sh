#!/bin/sh
/bin/cp /etc/project/settings.ini .
/usr/bin/wget https://bootstrap.pypa.io/get-pip.py

/usr/bin/docker-compose down



/usr/bin/docker-compose up --build -d