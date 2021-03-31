# mspr_project_back

![Django](https://pub.phyks.me/sdz/sdz/medias/uploads.siteduzero.com_files_386001_387000_386523.png)

[Télécharger](https://www.python.org/downloads/) et installer python

[Télécharger](https://www.postgresql.org/download/windows/) et installer postgresql & pgadmin

# Basculer sur la branche develop 
git checkout develop

# Installer virtualenv et django
`pip install virtualenv`
`pip install django`


# Créer virtualenv
`vitualenv my_venv`


# Activer virtualenv
`my_venv\Scrits\activate`


# Installer les librairies
`pip install -r requirements.txt`

# Créer une base de donnée sur pgadmin ou via plsql
Changer vos identifiants de base de données et le nom de la base de données dans le app/.env

# Créer les migrations et appliquer
`pip manage.py makemigrations api`
`pip manage.py migrate`

# Créer un super utilisateur
`pip manage.py createsuperuser`


# Lancer le serveur
`pip manage.py runserver`

 # Adresses utiles
## [api](http://127.0.0.1:8000/)
## [admin](http://127.0.0.1:8000/admin)
