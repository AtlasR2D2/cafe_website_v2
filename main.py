from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import pandas as pd
import datetime
from flask_sqlalchemy import SQLAlchemy


COFFEE_EMOJI = "☕"
WIFI_EMOJI = "💪"
NOT_AVAILABLE_EMOJI = "✘"
POWER_EMOJI = "🔌"
MAX_STARS = 5


def generate_stars(star_icon, num: int):
    """Generates a concatenated string of num star icons"""
    star_string = ""
    if num == 0:
        star_string = NOT_AVAILABLE_EMOJI
    else:
        for i in range(num):
            star_string += star_icon
    # Output String
    return star_string

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), unique=False, nullable=False)
    img_url = db.Column(db.String(500), unique=False, nullable=False)
    location = db.Column(db.String(250), unique=False, nullable=False)
    has_sockets = db.Column(db.Boolean, unique=False, nullable=False)
    has_toilet = db.Column(db.Boolean, unique=False, nullable=False)
    has_wifi = db.Column(db.Boolean, unique=False, nullable=False)
    can_take_calls = db.Column(db.Boolean, unique=False, nullable=False)
    seats = db.Column(db.String(250), unique=False, nullable=True)
    coffee_price = db.Column(db.String(250), unique=False, nullable=True)
    def get_data(self):
        return {field: value for (field, value) in self.__dict__.items() if field != "_sa_instance_state"}
    def get_headers(self):
        strSQL = "SELECT p.[name] as [column_name] FROM sqlite_master AS m " \
                 "INNER JOIN pragma_table_info(m.[name]) AS p " \
                 "WHERE m.[name] = 'cafe' " \
                 "ORDER BY p.[cid]"
        return [row[0] for row in db.engine.execute(strSQL)]
    def get_bool_headers(self):
        strSQL = "SELECT p.[name] as [column_name] FROM sqlite_master AS m " \
                 "INNER JOIN pragma_table_info(m.[name]) AS p " \
                 "WHERE m.[name] = 'cafe' and p.[type]='BOOLEAN' " \
                 "ORDER BY p.cid"
        return [row[0] for row in db.engine.execute(strSQL)]

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Location URL', validators=[DataRequired(), URL()])
    open_time = TimeField("What time does the cafe open (HH:MM)?", validators=[DataRequired()])
    closing_time = TimeField("What time does the cafe close (HH:MM)?", validators=[DataRequired()])
    coffee_rating = SelectField(choices=[generate_stars(COFFEE_EMOJI, num) for num in range(MAX_STARS+1)], validators=[DataRequired()])
    wifi_rating = SelectField(choices=[generate_stars(WIFI_EMOJI, num) for num in range(MAX_STARS + 1)], validators=[DataRequired()])
    power_rating = SelectField(choices=[generate_stars(POWER_EMOJI, num) for num in range(MAX_STARS + 1)], validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/cafes', methods=["GET", "POST"])
def cafes():
    cafe_data_q = Cafe.query.order_by(Cafe.id).all()
    cafe_headers = cafe_data_q[0].get_headers()
    bool_headers = cafe_data_q[0].get_bool_headers()
    # print(cafe_headers)
    cafe_data = []
    for cafe_x in cafe_data_q:
        cafe_data.append(cafe_x.get_data())
    print(cafe_data)
    # Replace boolean fields with yes/no
    for cafe in cafe_data:
        for field in bool_headers:
            if cafe[field]:
                cafe[field] = "Yes"
            else:
                cafe[field] = "No"
    csv_data = pd.read_csv('./cafe-data.csv', encoding="utf-8")
    data_headers = list(csv_data.columns)
    data = csv_data.values.tolist()

    return render_template('cafes.html', cafes=cafe_data, headers=cafe_headers)
    # return render_template('cafes.html', cafes=data, headers=data_headers)


if __name__ == '__main__':
    app.run(debug=True)

