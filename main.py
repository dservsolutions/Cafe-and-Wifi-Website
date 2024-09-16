import json

from flask import render_template, Flask, request, flash, url_for, jsonify
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
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)



with app.app_context():
    db.create_all()

def index_card():
    query = db.session.execute(db.select(Cafe))
    result = query.scalars().all()
    items = [ data for data in result]
    return items

@app.route('/')
def home():
    items = index_card()
    item_1 = items[0]
    item_2 = items[1]
    return render_template('index.html', first_card = item_1, second_card = item_2)


@app.route('/all_places')
def view_all():
    query = db.session.execute(db.select(Cafe))
    result = query.scalars().all()
    return render_template('all_places.html', places=result)

@app.route('/edit/', methods=["POST", "GET"])
def edit_places():
    # if request.method == 'POST':
    #     place_id = request.form.get('id')
    #     place_to_update = db.get_or_404(Cafe, place_id)
        return render_template('edit.html')


@app.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "POST":
        data = request.form
        if data['toilet'] == "None":
            has_toilet = 0
        elif data['wifi'] == "None":
            has_wifi = 0
        else:
            has_toilet = 1
            has_wifi = 1
            print(f"{has_toilet},{has_wifi}")

        # name = request.form['name']
        # map_url = request.form['map_url']
        # img_url = request.form['img_url']
        # location = request.form['location']
        # seats = request.form['seats']
        # coffee_price = request.form['coffe_price']


        # has_wifi = request.form['has_wifi']
        # has_sockets = request.form['has_sockets']
        # can_take_calls = request.form['can_take_calls']

        # new_place = Cafe(
        #     name = request.form['name'],
        #     map_url = request.form['map_url'],
        #     img_url = request.form['img_url'],
        #     location = request.form['location'],
        #     seats = request.form['seats'],
        #     coffee_price = request.form['coffe_price'],
        #     has_toilet = request.form['checked'],
        #         has_wifi = request.form['checked'],
        #     has_sockets = request.form['check'],
        #     can_take_calls = request.form['can_take_calls']
        # )
        # db.session.add(new_place)
        # db.session.commit()


        return redirect(url_for('home'))
    return render_template('add.html')

if __name__ == "__main__":
    app.run(debug=True)
