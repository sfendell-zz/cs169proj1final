# Create your views here.
import json
from django.http import HttpResponse
from models import UsersModel, SUCCESS, ERR_BAD_CREDENTIALS, ERR_USER_EXISTS, ERR_BAD_USERNAME, ERR_BAD_PASSWORD


def login(request):
    if request.method == 'POST':
        request_data = request.POST
        responseInt = UsersModel.login(**request_data)
        if responseInt == ERR_BAD_CREDENTIALS:
            response_data = {'errCode' : ERR_BAD_CREDENTIALS}
        elif responseInt > 0:
            response_data = {'errCode' : SUCCESS,
                    'count' : responseInt}
        else:
            raise Exception('Bad response from server!')
        return HttpResponse(json.dumps(response_data), content_type = "application/json")
    else:
        raise Exception('Request must be a post!')
    
def add(request):
    if request.method == 'POST':
        request_data = request.POST
        responseInt = UsersModel.login(**request_data)
        if responseInt in [ERR_USER_EXISTS, ERR_BAD_USERNAME, ERR_BAD_PASSWORD]:
            response_data = {'errCode' : responseInt}
        elif responseInt > 0:
            response_data = {'errCode' : SUCCESS,
                             'count' : responseInt}
        else:
            raise Exception('Bad response from server!')
        return HttpResponse(json.dumps(response_data), content_type = "application/json")
    else:
        raise Exception('Request must be a post!')

def resetFixture(request):
    return {'errCode' : UsersModel.TESTAPI_resetFixture()}

def unitTests(request):
    return {'totalTests' : 0,
            'nrFailed'   : 0,
            'output'     : None}
