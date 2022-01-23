from authlib.integrations.flask_client import OAuth
from flask import redirect, url_for, session, request

# decorator for routes that should be accessible only by logged in users
from .oauth_deco import login_is_required
from project import app

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="228951075563-jqqbi0rkk0ba5g4lo51pqt3188lqi9pv.apps.googleusercontent.com",
    client_secret="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",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/glogin')
def glogin():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/callback')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/room')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)

    return redirect('/')
