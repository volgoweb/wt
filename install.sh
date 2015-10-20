#! /bin/bash
python manage.py flush
python manage.py syncdb
python manage.py demo_data
python manage.py loaddata sitetree.json
