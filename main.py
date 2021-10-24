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

# new_book = Movie(title="Phone Booth", year="2002",
#                  description="Publicist Stuart Shepard finds himself trapped in a phone booth, "
#                              "pinned down by an extortionist's sniper rifle. Unable to leave or receive "
#                              "outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#                  rating=7.3, ranking=10, review="My favourite character was the caller.",
#                  img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")
# db.session.add(new_book)
# db.session.commit()
all_movies = []


@app.route("/")
def home():
    all_movies = Movie.query.all()
    return render_template("index.html", movies=all_movies)


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
        return render_template('add.html', movie_list=movie_data.json()['results'])
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
    return render_template('edit.html', movie=get_movie, form=edit_form)


if __name__ == '__main__':
    app.run(debug=True)
