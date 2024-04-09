@echo off
del /f /q db.sqlite3
del /f /q home\migrations\0001_initial.py

@REM create the migrations
python reset_sqlite.py
python manage.py makemigrations
python manage.py migrate
python initdb.py