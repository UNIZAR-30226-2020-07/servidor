# Servidor

# Instalation

* `pip install django`
* `pip install djangorestframework `
* `pip install django-rest-auth`
* `pip install django-allauth`
* `pip install drf-yasg`

# Recreate database

* delete files under all migrations folders with the name format  XXXX_initial.py (been the X's a succesion of numbers),  
* and the db.sqlite3 file 
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py loaddata initial_data`
