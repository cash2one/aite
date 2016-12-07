# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from weibo import APIClient,APIError
from aite.settings import app_id,app_secret
from datetime import datetime, tzinfo, timedelta

from .models import users
import json,time
# Create your views here.
@ensure_csrf_cookie
def index(request):
    if _check_cookie(request):
        uid, access_token, expired_time = _check_cookie(request)
        u = users.objects.filter(uid=uid)[0]
        return render_to_response('index.html',{'user':u})
    else:
        return render_to_response('signin.html')

@ensure_csrf_cookie
def signin(request):
    client = _create_client()
    return redirect(client.get_authorize_url())

def signout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    return redirect('/')

def callback(request):
    code = request.GET.get('code')
    client = _create_client()
    r = client.request_access_token(code)
    # logging.info('access token: %s' % json.dumps(r))
    access_token, expires_in, uid = r.access_token, r.expires_in, r.uid
    client.set_access_token(access_token, expires_in)
    u = client.users.show.get(uid=uid)
    # logging.info('got user: %s' % uid)
  
    try:
        user = users.objects.filter(uid=uid)[0]
        user.name = u.screen_name
        user.image_url = u.avatar_large or u.profile_image_url
        user.statuses_count = u.statuses_count
        user.friends_count = u.friends_count
        user.followers_count = u.followers_count
        user.verified = u.verified
        user.verified_type = u.verified_type
        user.auth_token = access_token
        user.expired_time = expires_in
        user.save()
      
    except Exception,e:
        print str(e)
        p = users.objects.create(name=u.screen_name, \
            image_url=u.avatar_large or u.profile_image_url, \
            statuses_count=u.statuses_count, \
            friends_count=u.friends_count, \
            followers_count=u.followers_count, \
            verified=u.verified, \
            verified_type=u.verified_type, \
            auth_token=access_token, \
            expired_time=expires_in,
            uid=uid)
    request.session['uid'] = uid
    request.session['access_token'] = access_token
    request.session.set_expiry(expires_in)
    return redirect('/')

def update(request):
    if request.method == 'POST':
        if _check_cookie(request):
            uid,access_token,expired_time = _check_cookie(request)
            client = _create_client()
            client.set_access_token(access_token,expired_time)
            try:
                r = client.statuses.update.post(status=request.POST.get('status'))
                print r
                if 'error' in r:
                    return r
                return HttpResponse(json.dumps({'data': 'ok'}),
                                    content_type="application/json")
            except APIError, e:
                return HttpResponse(json.dumps({'error': str(e)}),
                                    content_type="application/json")
        else:
            return render_to_response('signin.html')
def update_p(request):
    if request.method == 'POST':
        if _check_cookie(request):
            uid,access_token,expired_time = _check_cookie(request)
            client = _create_client()
            client.set_access_token(access_token,expired_time)
            try:
                r = client.statuses.upload.post(status=request.POST.get('status'))
                print r
                if 'error' in r:
                    return r
                return HttpResponse(json.dumps({'data': 'ok'}),
                                    content_type="application/json")
            except APIError, e:
                return HttpResponse(json.dumps({'error': str(e)}),
                                    content_type="application/json")
        else:
            return render_to_response('signin.html')

def friends(request):
    if request.method == 'POST':
        if _check_cookie(request):
            uid,access_token,expired_time = _check_cookie(request)
            client = _create_client()
            client.set_access_token(access_token,expired_time)
            try:
                r = client.friendships.friends.get(uid=uid, count=99)
                return HttpResponse(json.dumps({'data':[_format_user(u) for u in r.users]}), content_type="application/json")
            except APIError, e:
                return HttpResponse(json.dumps({'error': str(e)}),
                                    content_type="application/json")
                
        else:
            return render_to_response('signin.html')

def load(request):
    if request.method == 'POST':
        if _check_cookie(request):
            uid,access_token,expired_time = _check_cookie(request)
            client = _create_client()
            client.set_access_token(access_token,expired_time)
            try:
                r = client.statuses.home_timeline.get()
                return  HttpResponse(json.dumps({'data':[_format_weibo(s) for s in r.statuses]}), content_type="application/json")
            except APIError, e:
                return HttpResponse(json.dumps({'error': str(e)}),
                                    content_type="application/json")
        else:
             return render_to_response('signin.html')

def hint(request):
    if request.method == 'POST':
        if _check_cookie(request):
            uid,access_token,expired_time = _check_cookie(request)
            client = _create_client()
            client.set_access_token(access_token,expired_time)
            try:
                return HttpResponse(json.dumps({'data':client.remind.unread_count.get()}),content_type="application/json")

            except APIError, e:
                return HttpResponse(json.dumps({'error': str(e)}),
                                    content_type="application/json")
        else:
            return render_to_response('signin.html')

def _check_cookie(request):
    uid = request.session.get('uid', False)
    if uid:
        access_token = request.session['access_token']
        expired_time = request.session.get_expiry_age()
        return uid,access_token,expired_time
    else:
        return False
    
def _create_client():
    return APIClient(app_id, app_secret, redirect_uri='http://52kantu.cn/callback')

_TD_ZERO = timedelta(0)
_TD_8 = timedelta(hours=8)

class UTC8(tzinfo):
    def utcoffset(self, dt):
        return _TD_8

    def tzname(self, dt):
        return "UTC+8:00"

    def dst(self, dt):
        return _TD_ZERO

_UTC8 = UTC8()

def _format_datetime(dt):
    t = datetime.strptime(dt, '%a %b %d %H:%M:%S +0800 %Y').replace(tzinfo=_UTC8)
    return time.mktime(t.timetuple())

def _format_user(u):
    return dict(id=str(u.id), screen_name=u.screen_name, profile_url=u.profile_url, verified=u.verified, verified_type=u.verified_type, profile_image_url=u.profile_image_url)

def _format_weibo(st):
    user = st.user
    r = dict(
        user = _format_user(st.user),
        text = st.text,
        created_at = _format_datetime(st.created_at),
        reposts_count = st.reposts_count,
        comments_count = st.comments_count,
    )
    if 'original_pic' in st:
        r['original_pic'] = st.original_pic
    if 'thumbnail_pic' in st:
        r['thumbnail_pic'] = st.thumbnail_pic
    if 'retweeted_status' in st:
        r['retweeted_status'] = _format_weibo(st.retweeted_status)
    return r


