# REST API application made with flask.

Contains <> branches

Final and stable application is in the master branch

NOTE: Use a virtual environment with python 3.9 to run the application

## INSATLLATION

Run the following command to install dependencies:

```
pip install -r requirements.txt
```

## RUN

Run the following command to start the application:

```
python app.py
```

## IMPORTANT

Make sure to delete the `data.db` file from `database` directory before fresh run.

## Steps to database migration

1. ```
   flask db init
   ```

   To initiate migration process.

2. Edit the `alembic.ini` and `env.py` according to requirements.
3. ```
   flask db migrate
   ```
   To create migration instance.
4. Edit the version file accordingly.
5. ```
   flask db upgrade
   ```
   To commit the upgrade.
