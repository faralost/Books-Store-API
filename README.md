# Books-Store-API

----Small api app for books store---

To start project install python version 3.9 and pip

After cloning move to cloned directory and run the folllowing commands:

Create virtual environment:
```bash
python -m venv venv
```

Activate virtual environment
```bash
source venv/bin/activate:
or
venv\Scripts\activate (Windows)
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Apply the migrations:
```bash
./manage.py migrate
```

Download the fixtures:
```bash
./manage.py loaddata fixtures/auth.json
./manage.py loaddata fixtures/dump.json
```

Create a database in PostgreSQL, and then create an .env file in the project directory and fill it in as follows:


SECRET_KEY=django_secret_key

DEBUG=(1 for True, 0 for False)

POSTGRES_DB=db_name

POSTGRES_USER=db_user_name

POSTGRES_PASSWORD=db_user_password

POSTGRES_PORT=db_port

POSTGRES_HOST=db_host

SOCIAL_AUTH_GITHUB_KEY=your_social_auth_github_key

SOCIAL_AUTH_GITHUB_SECRET=your_social_auth_github_secret


To start the server run:
```bash
./manage.py runserver
```

To access the admin panel, go to http://localhost:8000/admin
(passwords of the created users correspond to their usernames)