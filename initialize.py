import os
import sys
from data_access import create_views


# makemigratsion
os.system("python manage.py makemigrations")
os.system("python manage.py migrate")

# create database views
create_views()
