from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String, nullable=False)
    movie_picture_url = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)



    def __init__(self, movie_title, movie_picture_url,description, rating):
        self.movie_title = movie_title
        self.movie_picture_url = movie_picture_url
        self.description = description
        self.rating = rating


class MovieSchema(ma.Schema):
    class Meta:
        fields = ("id", "movie_title", "movie_picture_url", "description", "rating");
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@app.route("/movie/add", methods=["POST"])
def add_movie():
    movie_title = request.json.get("movie_title")
    movie_picute_url = request.json.get("movie_picture_url")
    description = request.json.get("description")
    rating = request.json.get("rating")

 
    record = Movies(movie_title, movie_picute_url, description, rating)
    db.session.add(record)
    db.session.commit()

    return jsonify(movie_schema.dump(record))

@app.route("/movie/get", methods=["GET"])
def get_all_movies():
    all_movies = Movies.query.all()
    return jsonify(movies_schema.dump(all_movies))

@app.route("/movie/<id>", methods=["GET"])
def get_movie(id):
    movie = Movies.query.get(id)
    return movie_schema.jsonify(movie)

@app.route("/movie/<id>", methods=["PUT"])
def movie_update(id):
    movie = Movies.query.get(id)
    movie_title = request.json['movie_title']
    movie_picture_url = request.json['movie_picture_url']
    description = request.json['description']
    rating = request.json['rating']


    movie.movie_title = movie_title
    movie_picture_url = movie_picture_url
    description = description
    rating = rating

    db.session.commit()
    return movie_schema.jsonify(movie) 


@app.route("/movie/<id>", methods=["DELETE"])
def movie_delete(id):
    movie = Movies.query.get(id)
    db.session.delete(movie)
    db.session.commit()

    return "movie was successfully deleted"

if __name__ == "__main__":
    app.run(debug=True)