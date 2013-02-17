# Create your views here.
import json, traceback, tempfile, os, re
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
        elif request.method == 'GET':
            return 'asdf'
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
    (_, ofileName) = tempfile.mkstemp(prefix="userCounter")
    try:
        errMsg = ""     # We accumulate here error messages
        output = ""     # Some default values
        totalTests = 0
        nrFailed   = 0
        while True:  # Give us a way to break
            # Find the path to the server installation
            os.system("cd ../")
            cmd = "make unit_tests > "+ofileName+" 2>&1"
            print "Executing "+cmd
            code = os.system(cmd)
            if code != 0:
                # There was some error running the tests.
                # This happens even if we just have some failing tests
                errMsg = "Error running command (code="+str(code)+"): "+cmd+"\n"
                # Continue to get the output, and to parse it
                
            # Now get the output
            try:
                ofileFile = open(ofileName, "r")
                output = ofileFile.read()
                ofileFile.close ()
            except:
                errMsg += "Error reading the output "+traceback.format_exc()
                # No point in continuing
                break
            
            print "Got "+output
            # Python unittest prints a line like the following line at the end
            # Ran 4 tests in 0.001s
            m = re.search(r'Ran (\d+) tests', output)
            if not m:
                errMsg += "Cannot extract the number of tests\n"
                break
            totalTests = int(m.group(1))
            # If there are failures, we will see a line like the following
            # FAILED (failures=1)
            m = re.search('rFAILED.*\(failures=(\d+)\)', output)
            if m:
                nrFailed = int(m.group(1))
            break # Exit while

        # End while
        resp = { 'output' : errMsg + output,
                 'totalTests' : totalTests,
                 'nrFailed' : nrFailed }
        response = HttpResponse(json.dumps(resp), content_type = "application/json")
        return response
    finally:
        os.unlink(ofileName)

from django.template.loader import get_template
from django.template import Context


'''
def users(request):

    t = get_template('users.html')
    print 'got template'
    html = t.render(Context(None))
    print 'rendered template'
    resp = HttpResponse(html)
    print 'made httpresponse'
    return resp

def clientcss(request):
    t = get_template('client.css')
    html = t.render(Context(None))
    resp = HttpResponse(html)
    return resp

def clientjs(request):
    t = get_template('client.js')
    html = t.render(Context(None))
    resp = HttpResponse(html)
    return resp
'''
def _template(template_page):
    return HttpResponse(get_template(template_page).render(Context(None)))

def users(request):
    return _template('users.html')

def clientcss(request):
    return _template('client.css')

def clientjs(request):
    return _template('client.js')
