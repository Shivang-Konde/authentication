from functools import wraps
import pymongo
import jwt
from django.conf import settings
from django.http import HttpResponse


def requireLogin(to_authenticate_fn):

    @wraps(to_authenticate_fn)
    def inner(request, *args, **kwargs):

        token = request.headers.get('token', None)

        if verify_token(token):
            # TODO: check if email is present in database
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            req_user=jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            mydb = myclient["mydb"]
            userColl = mydb['users']
            userObj = userColl.find_one({'email':req_user['email']})
    
            if userObj['password']==req_user['password']:
                return to_authenticate_fn(request, *args, **kwargs)
        else:
            return HttpResponse('Unauthorized', status=401)

    return inner


def verify_token(token):

    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
    except:
        return None

    return {'email': data['email']}