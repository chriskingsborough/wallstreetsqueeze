# refresh info on saturdays
if [ "$(date +%u)" = 6 ]; then python database/refresh_info.py; fi
