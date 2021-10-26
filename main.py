from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from edit_form import EditForm
from add_form import AddForm
import requests

app = Flask(__name__)
MOVIEDB_API_KEY = '4727a0d9e160a8630555cd67e57115e9'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float(10), nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(100), nullable=False)
# db.create_all()
# https://image.tmdb.org/t/p/w500/

all_movies = []


@app.route("/")
def home():
    all_movies = Movie.query.all()
    return render_template("index.html", movies=all_movies)


@app.route('/add-movie')
def add_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:

        new_movie = Movie(
            title=request.args.get('title'),
            # The data in release_date includes month and day, we will want to get rid of.
            year=request.args.get('year').split('-')[0], rating=0, ranking=0, review="Not reviewed yet",
            img_url=f"https://image.tmdb.org/t/p/w500/{request.args.get('img_url')}",
            description=request.args.get('overview')
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(f"/edit?id={movie_api_id}")


@app.route('/add', methods=['POST', 'GET'])
def add_page():
    add_form = AddForm()
    if request.method == 'POST':
        params = {
            "api_key": '4727a0d9e160a8630555cd67e57115e9',
            'language': 'en-US',
            'query': add_form.title.data,
            'include_adult': 'true'

        }
        movie_data = requests.get(url="https://api.themoviedb.org/3/search/movie", params=params)
        return render_template('select.html', movie_list=movie_data.json()['results'])
    return render_template('add.html', form=add_form)


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect('/')


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    edit_form = EditForm()
    movie_id = request.args.get("id")
    get_movie = Movie.query.filter_by(id=movie_id).first()
    if request.method == 'POST':
        movie_to_update = Movie.query.get(request.form['id'])
        movie_to_update.rating = edit_form.rating.data
        movie_to_update.review = edit_form.review.data
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', movie=get_movie, form=edit_form, movie_id=movie_id)


if __name__ == '__main__':
    app.run(debug=True)
