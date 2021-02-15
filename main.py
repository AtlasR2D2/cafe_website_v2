from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import datetime
from flask_sqlalchemy import SQLAlchemy

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

    return render_template('cafes.html', cafes=cafe_data, headers=cafe_headers)


if __name__ == '__main__':
    app.run(debug=True)

