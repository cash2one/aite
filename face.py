# -*- coding: utf-8 -*-

import requests


baseurl = 'https://api-cn.faceplusplus.com/facepp/v3'
api_key = ''
api_secret = ''
class APIError(StandardError):
    '''
    raise APIError if receiving json message indicating failure.
    '''
    def __init__(self, error_msg, request):
        self.error_msg = error_msg
        self.request = request
        StandardError.__init__(self, error_msg)

    def __str__(self):
       return 'APIError: %s, request: %s' % (self.error_msg, self.request)

def http_call(url,params,method='POST'):
    if method == 'POST':
        theurl = '%s/%s' %(baseurl,url)
        if 'image_file' in params or 'image_file1' in params:
            pass
        else:
            params.update(api_key=api_key,api_secret=api_secret)
            z = requests.post(theurl,data=params)
            zjson = z.json()
            if z.status_code == '200':
                return zjson
            else:
                raise APIError(zjson['error_msg'],url)

class faceset():
    def create(self):
        params = {}
        z = http_call('faceset/create',params)
        if 'error_message' in z:
            return z
        else:
            faceset_token = z['faceset_token']
            face_count = z['face_count']
            # sql insert
    def add(self,image_url):
        params = {}
        faceset_token = '' #从数据库获取，
        face_tokens = detect(image_url)
        params.update(faceset_token=faceset_token,face_tokens=face_tokens)
        if 'error_message' in face_tokens:
            pass
        else:
            z = http_call('faceset/addface',params)
            if 'error_message' in z:
                pass
            else:
                faceset_token = z['faceset_token']
                face_count = z['face_count']
                face_added = z['face_added']
                if face_added == 1:
                    # sql update
                    pass
                else:
                    #返回加入失败的原因
                    return z['failure_detail']
                    
    def remove(self,uid):
        params = {}
        faceset_token = '' #根据uid 从数据库获取
        face_tokens = '' #根据uid 从数据库获取
        params.update(faceset_token=faceset_token,face_tokens=face_tokens)
        z = http_call('faceset/removeface',params)
        if 'error_message' in z:
            pass
        else:
            faceset_token = z['faceset_token']
            face_count = z['face_count']
            face_removed = z['face_removed']
            if face_removed == 1:
                # sql update
                pass
            else:
                #返回加入失败的原因
                return z['failure_detail']
    def update(self):
        pass
    def detail(self):
        pass
    def delete(self):
        pass
    def getsets(self):
        pass

def detect(image_url):
    params = {}
    params['image_url'] = image_url
    # 默认不返回人脸五官和轮廓的83个关键点。
    params['return_landmark'] = 1
    z = http_call('detect',params)
    if 'error_message' in z:
            return z
    else:
        if len(z['faces']) > 1:
            return {'error_message':u'人脸有超过1张'}
        else:
            return {'face_tokens':z['faces']['face_token']}
def search(image_url):
    params = {}
    faceset_token = ''
    params.update(faceset_token=faceset_token,image_url=image_url)
    z = http_call('search',params)
    if 'error_message' in z:
            return z
    else:
        if len(z['results']) != 0:
            face_token = z['results']['face_token']
            confidence = z['results']['confidence']






