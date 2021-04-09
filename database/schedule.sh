# refresh info on saturdays
if [ "$(date +%u)" = 6 ]; then python database/refresh_info.py; fi
if [ "$(date +%u)" = 6 ]; then python database/refresh_view_collections.py; fi
# refresh collections on the 1st of the month
if [ "$(date +%d)" = 1 ]; then python database/refresh_collections.py; fi
