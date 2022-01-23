import uuid

from flask import render_template, request, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from .oauth_deco import login_is_required
from project import app, db
from .models import User, Room
from project import oauth

@app.route('/')
def index():
    return render_template('index.html', session=session)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Вже зареєстровано користувача з такою адресою')
            return redirect(url_for('register'))

        newUser = User(email=email, password=generate_password_hash(password, method='sha256'))
        try:
            db.session.add(newUser)
            db.session.commit()
            flash("Користувача успішно зареєстровано")
            return redirect(url_for('login'))
        except:
            return "Error adding new User to DB"
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        remember = True if request.form.get('remember') else False

        if not user or not check_password_hash(user.password, password):
            flash("Перевірте правильність данних")
            return redirect(url_for('login'))
        session.permanent = remember
        session['profile'] = email
        return redirect(url_for('room'))


@app.route('/room', methods=['GET', 'POST'])
@login_is_required
def room():
    if request.method == 'POST':
        roomNum = request.form['n_groop']
        room = Room.query.filter_by(room=roomNum).first()
        if room:
            return redirect(url_for('room') + "/" + room.url)
        # redirect('/room/<string:url>')
        else:
            url = uuid.uuid4().hex
            newRoom = Room(room=roomNum, url=url)
            try:
                db.session.add(newRoom)
                db.session.commit()
                flash("Кімнату створено")
                return redirect(url_for('room') + "/" + url)
            except:
                return "Error adding new User to DB"
    else:
        return render_template('room.html')

@app.route('/room/<path>/')
@login_is_required
def conf_room(path):
    roomName = Room.query.filter_by(url=path).first_or_404().room
    if(roomName):
        session['room'] = roomName
        return redirect('https://pe-to-pe.herokuapp.com/')
    else:
        return redirect('https://pe-to-pe.herokuapp.com/')
