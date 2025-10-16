from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from models import db, Users, Movie, Reservation

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/movie_db_new'
app.config['SECRET_KEY'] = 'secret123'
db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


def create_tables():
    with app.app_context():
        db.create_all()
        # Populate sample movies (if none exist)
        if not Movie.query.first():
            sample = [
                Movie(title='Inception', date='2025-10-09'),
                Movie(title='Interstellar', date='2025-10-10'),
                Movie(title='Tenet', date='2025-10-11')
            ]
            db.session.add_all(sample)
            db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('movies'))
        flash('Invalid credentials!')
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    user = Users(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    flash('User registered! Please login.')
    return redirect(url_for('login'))


@app.route('/movies')
@login_required
def movies():
    movies = Movie.query.all()
    reservations = {r.movie_id for r in Reservation.query.filter_by(user_id=current_user.id).all()}
    return render_template('movies.html', movies=movies, reserved=reservations)


@app.route('/reserve/<int:movie_id>', methods=['POST'])
@login_required
def reserve(movie_id):
    existing = Reservation.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if not existing:
        db.session.add(Reservation(user_id=current_user.id, movie_id=movie_id))
        db.session.commit()
        flash('Movie reserved!')
    else:
        flash('Already reserved.')
    return redirect(url_for('movies'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
