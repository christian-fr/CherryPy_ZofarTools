#!/bin/sh
/bin/cp /etc/project/settings.ini .

/usr/bin/docker-compose down

/usr/bin/docker-compose up --build -d