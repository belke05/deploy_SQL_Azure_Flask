# deploy_SQL_Azure_Flask

# config.py

```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ["DBHOST"]

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['DBUSER'],
    dbpass=os.environ['DBPASS'],
    dbhost=os.environ['DBHOST'],
    dbname=os.environ['DBNAME']
)

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['DBUSER'],
    dbpass=os.environ['DBPASS'],
    dbhost=os.environ['DBHOST'],
    dbname=os.environ['DBNAME']
    )

class TestingConfig(Config):
    TESTING = True
```

* can be used to determine the configuration variables of your app via the environment variable  APP_SETTINGS --- os.environ[‘APP_SETTINGS’] =’config.ProductionConfig’

# App.py 



```python
from flask import Flask, render_template, redirect, url_for, request
from sklearn.externals import joblib
from flask_sqlalchemy import SQLAlchemy
import os
import numpy as np
import requests
import json

app = Flask(__name__)
db = SQLAlchemy()
app.config.from_object(os.environ['APP_SETTINGS'])
# change the env variable app settings to switch from environment 
# as object it will use our config module
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# SQL alchemy is our Object relational mapper
import models


@app.route("/")
def index():
    return render_template("index.html", prediction=float(0))

@app.route("/predict", methods=['POST'])
def predict():
    if request.method=='POST':

        regressor = joblib.load("linear_regression_model.pkl")

        data = dict(request.form.items())

        years_of_experience = np.array(float(data["YearsExperience"])).reshape(-1,1)

        prediction = regressor.predict(years_of_experience)
        result = models.Result(
            YearsExperience=float(years_of_experience),
            Prediction = float(prediction)
        )
        db.session.add(result)
        db.session.commit()
    return render_template("index.html", prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)
```

* import to use models.Results otherwise you create circular dependencies 

# Manage.py

We will be able to both manage our application but also create so-called database migrations. Indeed, each time you make changes, you will need to migrate your database. So let's learn to do the thing

```python
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
# so you can do python manage.py db init upgrade or migrate 

if __name__ == '__main__':
    manager.run()
```

# define environment variables 

```bash
export DBPASS='something01'
export DBNAME='test_db'
export DBUSER='jedhauser@linear-regression-bdd-postgresql'
export DBHOST=myserver1000.postgres.database.azure.com 
export APP_SETTINGS="config.ProductionConfig"

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

python manage.py runserver
```

# create a virtualenv 

```
pip install virtualenv 
virtualenv virt -- creates a folder named virt 
source virt/Scripts/activate

python app.py 

pip install all the packages you need now
```

