from django.shortcuts import render
from django.shortcuts import render_to_response,redirect
from weibo import APIClient,APIError
from aite.settings import app_id,app_secret
from .models import users
# Create your views here.
def index(request):
    uid = request.session.get('uid', False)
    
    if uid:
        return render_to_response('index.html')
    else:
        return render_to_response('signin.html')
    
def _create_client():
    return APIClient(app_id, app_secret, redirect_uri='http://127.0.0.1:8000/callback')

def signin(request):
    client = _create_client()
    return redirect(client.get_authorize_url())

def callback(request):
    
    code = request.GET.get('code')
    client = _create_client()
    r = client.request_access_token(code)
    # logging.info('access token: %s' % json.dumps(r))
    access_token, expires_in, uid = r.access_token, r.expires_in, r.uid
    client.set_access_token(access_token, expires_in)
    u = client.users.show.get(uid=uid)
    # logging.info('got user: %s' % uid)
    users = db.select('select * from users where id=?', uid)
    user = dict(name=u.screen_name, \
            image_url=u.avatar_large or u.profile_image_url, \
            statuses_count=u.statuses_count, \
            friends_count=u.friends_count, \
            followers_count=u.followers_count, \
            verified=u.verified, \
            verified_type=u.verified_type, \
            auth_token=access_token, \
            expired_time=expires_in)
    if users:
        db.update_kw('users', 'id=?', uid, **user)
    else:
        user['id'] = uid
        db.insert('users', **user)
    _make_cookie(uid, access_token, expires_in)
    raise seeother('/')

