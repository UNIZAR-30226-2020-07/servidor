# Servidor

# Instalation

* `pip install django`
* `pip install djangorestframework `
* `pip install django-rest-auth`
* `pip install django-allauth`

# Recreate database

* delete files under all migrations folders and the db.sqlite3
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py loaddata initial_data`