#! /bin/bash
python manage.py flush --noinput
python manage.py syncdb --noinput
python manage.py demo_data
python manage.py loaddata sitetree.json
