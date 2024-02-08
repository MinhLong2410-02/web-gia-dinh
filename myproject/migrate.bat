@echo off
del /f /q db.sqlite3
@REM create the migrations
python manage.py makemigrations
python manage.py migrate
python initdb.py