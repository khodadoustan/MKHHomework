# [MKH Homework Project]

## Quick start

- Clone the repo
- Install requirements: `pip install -r requirements.txt`.
- Set variable environments: `export APP_SETTINGS=config.Config`.
- Create database on postgresql and set DATABASE_URL: `export  DATABASE_URL=postgresql:///sample_project`.
- Active virtualenv and run
  commands: ` python manage.py db init, python manage.py db migrate, python manage.py db upgrade`.
- Run project: `python app.py`.