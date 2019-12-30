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
