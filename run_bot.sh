#!/bin/bash
docker run --memory="1g" --restart unless-stopped -d -e TZ=Europe/Minsk -e APP_VERSION_TAG=$1 ialexofficial/commun-flat-by-bot:$1 python3 main.py
