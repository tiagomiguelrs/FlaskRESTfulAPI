from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from random import choice

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
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

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/search", methods=["GET"])
def search():
    cafe_location = request.args.get("loc")     # Gets the argument "loc" passed in the search bar "/search?loc=<loc>", of through postman
    result = db.session.execute(db.select(Cafe).where(Cafe.location == cafe_location).order_by(Cafe.name)).scalars()
    cafe_list = [cafe.to_dict() for cafe in result]
    return jsonify(cafe_list)

@app.route("/all", methods=["GET"])
def get_all():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars()
    cafe_list = [cafe.to_dict() for cafe in result]
    return jsonify(cafe_list)

@app.route("/random", methods=["GET"])  # the "GET" method is allowed by default, so there is no need to write "methods=["GET"]"
def get_random():
    result = db.session.execute(db.select(Cafe)).scalars()
    cafe_list = [cafe for cafe in result]
    cafe = choice(cafe_list)

# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add():
    new_entry = Cafe(name=request.form.get("name"),
                     map_url=request.form.get("map_url"),
                     img_url=request.form.get("img_url"),
                     location=request.form.get("location"),
                     seats=request.form.get("seats"),
                     has_toilet=bool(request.form.get("has_toilet")),
                     has_wifi=bool(request.form.get("has_wifi")),
                     has_sockets=bool(request.form.get("has_sockets")),
                     can_take_calls=bool(request.form.get("can_take_calls")),
                     coffee_price=request.form.get("coffee_price"))
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(response={"Success": "Successfully added a new cafe"})

# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    cafe_to_update = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    if cafe_to_update:
        cafe_to_update.coffee_price = request.form.get("coffee_price")      # Using the "form", it enables the use of "x-www-form-urlencoded" in postman
        db.session.commit()                                                 # Using the "args", it enables the use of "params" in postman
        return jsonify(success="Successfully updated the price.")
    else:   # Otherwise None
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."})

# HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def report_closed(cafe_id):
    api_key = request.form.get("api-key")
    if api_key == "TopSecretAPIKey":
        cafe_to_delete = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        if cafe_to_delete:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return jsonify(Ok={"Success": "The cafe was successfully deleted."})
        else:
            return jsonify(Error={"Not found": "Sorry, no cafe was found with that id."})
    else:
        return jsonify(Error={"Forbidden": "You don't have access to that command."})


if __name__ == '__main__':
    app.run(debug=True)
    db.session.close()
