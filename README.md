# Movie-Booking


1. Please install the requirement.txt 

```
$ pip install -r requirements.txt
```

2. Install postgresql Database

```
$ sudo apt update

$ sudo apt install postgresql postgresql-contrib

```

3. Create a database in PostgreSql

4. Change password in settings.py and add your database name

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yourdatabasename',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
    }
}

```

5. Migrate to database

```
$ python3 manage.py makemigrations

$ python3 manage.py migrate

```

6. Run Project

```
$ python3 manage.py runserver
```
