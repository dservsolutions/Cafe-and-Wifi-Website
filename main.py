import random
from crypt import methods

from flask import render_template, Flask, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, result_tuple, except_
from werkzeug.utils import redirect

app = Flask(__name__)


class Base(DeclarativeBase):
    pass

app.config['SECRET_KEY'] = "12345678"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)
                                                

# CAFE Table Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()

# def get_data():
#     while request.method == "POST":
#         data =  request.form
#         return data
#

@app.route('/')
def home():
    query = db.session.execute(db.select(Cafe.name))
    result = query.scalars().all()
    random_cafe = random.choice(result)
    return render_template('index.html', cafe=random_cafe)


@app.route('/places')
def view_all():
    query = db.session.execute(db.select(Cafe))
    result = query.scalars().all()
    return render_template('all_places.html', places=result)



@app.route('/add', methods=["POST", "GET"])
def add():
    return render_template('check.html')

if __name__ == "__main__":
    app.run(debug=True)
