from django.shortcuts import render
from django.shortcuts import render_to_response,redirect
from weibo import APIClient,APIError
from aite.settings import app_id,app_secret
from .models import users
# Create your views here.
def index(request):
    # if request.session.get['uid']:
    request.session.set_test_cookie()
    return render_to_response('index.html')
    # else:
    #     return redirect(signin)

def _create_client():
    return APIClient(app_id, app_secret, redirect_uri='http://127.0.0.1:8080')

def signin(request):
    client = _create_client()
    return redirect(client.get_authorize_url())

    