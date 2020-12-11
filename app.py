from flask import Flask, session, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegisterForm, SearchForm
from db import execute_read_query, execute_query
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/likes', methods=['GET', 'POST'])
def list_likes():
    if 'userID' not in session:
        return redirect(url_for('index'))

    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    
    user = session['userID']
    query = """SELECT song.songID, song.name FROM song, likes WHERE song.songID = likes.songID AND likes.userID = {};""".format(user)
    user_likes = execute_read_query(query)

    return render_template('likes.html', form=search, likes=user_likes)

@app.route('/listens', methods=['GET', 'POST'])
def list_listens():
    if 'userID' not in session:
        return redirect(url_for('index'))

    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    
    user = session['userID']
    query = """SELECT song.songID, song.name, listens.date_time FROM song, listens WHERE song.songID = listens.songID AND listens.userID = {};""".format(user)
    user_listens = execute_read_query(query)

    return render_template('listens.html', form=search, listens=user_listens)

@app.route('/track/<ID>', methods=['GET', 'POST'])
def songInfo(ID):
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    song = "SELECT song.*, album.genre, album.name, artist.name FROM song, album, artist WHERE song.artistID = artist.artistID AND song.albumID = album.albumID AND song.songID = {}".format(ID)
    result = execute_read_query(song)[0]
    if result:
        if 'userID' not in session:
            return render_template('track.html', form=search, data=result)
        else:
            user = session['userID']
            query = "SELECT * FROM likes WHERE userID = {} AND songID={};".format(user, ID)
            existing_like = execute_read_query(query)
            if existing_like:
                return render_template('track.html', session=session, existing_like=existing_like, form=search, data=result)
            else:
                return render_template('track.html', session=session, form=search, data=result)

    return "<h1>404</h1>"

@app.route('/artist/<ID>', methods=['GET', 'POST'])
def artistInfo(ID):
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    artist = "SELECT * FROM artist WHERE artistID = {}".format(ID)
    artist_info = execute_read_query(artist)[0]
    tracks = "SELECT songID, name FROM song WHERE artistID = {}".format(ID)
    tracks_list = execute_read_query(tracks)
    if artist_info:
        if 'userID' not in session:
            return render_template('artist.html', form=search, artist=artist_info, tracks=tracks_list)
        else:
            return render_template('artist.html', session=session, form=search, artist=artist_info, tracks=tracks_list)

    return "<h1>404</h1>"

@app.route('/album/<ID>', methods=['GET', 'POST'])
def albumInfo(ID):
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    album = "SELECT * FROM album WHERE albumID = {}".format(ID)
    album_info = execute_read_query(album)[0]
    tracks = "SELECT songID, name FROM song WHERE albumID = {}".format(ID)
    tracks_list = execute_read_query(tracks)
    if album_info:
        if 'userID' not in session:
            return render_template('album.html', form=search, album=album_info, tracks=tracks_list)
        else:
            return render_template('album.html', session=session, form=search, album=album_info, tracks=tracks_list)

    return "<h1>404</h1>"

@app.route('/add_listen/<ID>', methods=['GET', 'POST'])
def add_listens(ID):
    if 'userID' not in session:
        return redirect(url_for('index'))
    user = session['userID']
    currentTime = datetime.now()
    formatedTime = currentTime.strftime("%Y-%m-%d %X")
    query = """INSERT INTO `listens` (`userID`,`songID`,`date_time`) VALUES ("{}","{}","{}");""".format(user,ID,formatedTime)
    execute_query(query)
    return redirect(url_for('dashboard'))

@app.route('/add_likes/<ID>', methods=['GET', 'POST'])
def add_likes(ID):
    if 'userID' not in session:
        return redirect(url_for('index'))
    user = session['userID']
    query = "SELECT * FROM likes WHERE userID = {} AND songID={};".format(user, ID)
    existing_like = execute_read_query(query)
    if existing_like:
        query = "DELETE FROM likes WHERE userID = {} AND songID={};".format(user, ID)
        execute_query(query)
        return redirect(url_for('dashboard'))
    else:
        query = """INSERT INTO `likes` (`userID`,`songID`) VALUES ("{}","{}");""".format(user,ID)
        execute_query(query)
        return redirect(url_for('dashboard'))
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = "SELECT * FROM users WHERE email = '{}'".format(form.email.data)
        result = execute_read_query(user)[0]
        if result:
            if check_password_hash(result[4], form.password.data):
                session['firstName'] = result[1]
                session['lastName'] = result[2]
                session['userID'] = result[0]
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        email = form.email.data
        firstName = form.firstName.data
        lastName = form.lastName.data
        dob = form.dob.data
        new_user = "INSERT INTO `users`(`first_name`, `last_name`, `email`, `password`, `dob`) VALUES ('{}','{}','{}','{}','{}');".format(firstName, lastName, email, hashed_password, dob)
        print(new_user)
        execute_query(new_user)
        
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search_results(search):
    form = SearchForm(request.form)
    if form.validate_on_submit():
        search_string = search.data['search']

        search_songs_query = "SELECT songID, name FROM song WHERE name LIKE '%{}%';".format(search_string)
        songs_data = execute_read_query(search_songs_query)

        search_artists_query = "SELECT artistID, name FROM artist WHERE name LIKE '%{}%';".format(search_string)
        artist_data = execute_read_query(search_artists_query)

        search_album_query = "SELECT albumID, name FROM album WHERE name LIKE '%{}%';".format(search_string)
        album_data = execute_read_query(search_album_query)

    return render_template('search.html', form=form, songs_data=songs_data, artist_data=artist_data, album_data=album_data)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'userID' not in session:
        return redirect(url_for('index'))

    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    # Gathers a users last 10 listens
    query = """SELECT DISTINCT song.songID, song.name FROM song, listens WHERE song.songID = listens.songID AND listens.userID = {} ORDER BY date_time DESC LIMIT 10;""".format(session['userID'])
    top_10_listens = execute_read_query(query)

    # Gathers a users last 10 likes
    query = """SELECT song.songID, song.name FROM song, likes WHERE song.songID = likes.songID AND likes.userID = {} LIMIT 10;""".format(session['userID'])
    top_10_likes = execute_read_query(query)

    # Gathers a users top 10 likes
    # query = """SELECT DISTINCT song.songID, song.name FROM song, listens WHERE song.songID = listens.songID AND listens.userID = {} ORDER BY date_time DESC LIMIT 10;""".format(session['userID'])
    # top_10_listens = execute_read_query(query)

    return render_template('dashboard.html', form=search, listens=top_10_listens, likes=top_10_likes, name=session['firstName'] + " " + session['lastName'])

@app.route('/logout')
def logout():
    session.pop('userID', None)
    session.pop('firstName', None)
    session.pop('lastName', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
