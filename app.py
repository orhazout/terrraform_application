from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_cors import CORS
import psycopg2
import json
import os 


app = Flask(__name__)
app.config['SECRET_KEY'] = "my is secret key"
CORS(app)

db_host = "10.0.1.10"
db_port = 5432
db_name = "dogspatroldb"
db_user = "orhazout"
db_password = os.environ.get("DB_PASSWORD", "")

def create_connection():
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    return conn


class NameForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    weight = StringField("Weight", validators=[DataRequired()])
    time = StringField("Time", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/')
def home():
    return render_template('page.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    conn = create_connection()
    cur = conn.cursor()
    name = None
    form = NameForm()
    if form.validate_on_submit():
        pets = None
        if pets is None:
            cur.execute("INSERT INTO data (name, weight_value, mytime) VALUES (%s, %s, %s)", (form.name.data, form.weight.data, form.time.data))
            conn.commit()
            cur.close()
        conn.close()
        name = form.name.data
        form.name.data = ''
        form.weight.data = ''
        form.time.data = ''`
    cur.execute("SELECT * FROM data")
    our_pets= cur.fetchall()
    cur.close()
    conn.close()
    return render_template("data.html", form = form, name = name, our_pets=our_pets)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
