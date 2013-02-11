# Create your views here.
import json, traceback, tempfile, os
from django.http import HttpResponse
from models import UsersModel, SUCCESS, ERR_BAD_CREDENTIALS, ERR_USER_EXISTS, ERR_BAD_USERNAME, ERR_BAD_PASSWORD
from django.views.decorators.csrf import csrf_exempt                                          

@csrf_exempt
def login(request):
    if request.method == 'POST':
        request_data = json.loads(request.POST.keys()[0])
        try:
            responseInt = UsersModel.login(**request_data)
        except:
            print traceback.format_exc()
            raise
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
    
@csrf_exempt
def add(request):
    try:
        if request.method == 'POST':
            request_data = json.loads(request.POST.keys()[0])
            responseInt = UsersModel.add(**request_data)
            if responseInt in [ERR_USER_EXISTS, ERR_BAD_USERNAME, ERR_BAD_PASSWORD]:
                response_data = {'errCode' : responseInt}
            elif responseInt > 0:
                response_data = {'errCode' : SUCCESS,
                                 'count' : responseInt}
            else:
                print responseInt, ' was the response int'
                raise Exception('Bad response from server!')
            return HttpResponse(json.dumps(response_data), content_type = "application/json")
        else:
            raise Exception('Request must be a post!')
    except:
        print traceback.format_exc()
@csrf_exempt
def resetFixture(request):
    response = HttpResponse(json.dumps({'errCode' : UsersModel.TESTAPI_resetFixture()}), content_type = "application/json")
    print str(response)
    return response

@csrf_exempt
def unitTests(request):
    thisDir = os.path.dirname(os.path.abspath(__file__))
    (ofile, ofileName) = tempfile.mkstemp(prefix='unittestout')
    cmd = "python " + os.path.join(thisDir, '../manage.py') + ' test &> ' + ofileName 
    print "Executing " + cmd
    try:
        code = os.system(cmd)
        if code!=0:
            raise Exception("Something went wrong running the tests! The cmd %s did not work." % cmd)    
        with open(ofileName,'r') as ofile:
            firstLine = ofile.readline().strip()
        with open(ofileName,'r') as ofile:
            testout = ofile.read()
        total = len(firstLine)
        failures = total - firstLine.count('.')
        respDict = { 'totalTests' : total,
                     'nrFailed'   : failures,
                     'output'     : testout}
        response = HttpResponse(json.dumps(respDict), content_type = "application/json")
        return response
    except:
        print traceback.format_exc()
        raise