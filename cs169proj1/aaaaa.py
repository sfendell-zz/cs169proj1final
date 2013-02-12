"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'cs169.mysite.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

from django.test import TestCase
from models import *
#from django.core import management
#import cs169.mysite.settings as settings; 
#management.setup_environ(settings)
base_dir = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cs169_miniproject',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


def printToFile(msg):
    log_file = os.path.join(base_dir, 'test.log') 
    with open(log_file, 'a') as f:
        f.write(str(msg))
        
class Test(TestCase):


    def setUp(self):
        log_file = os.path.join(base_dir, 'test.log') 
        with open(log_file, 'w') as f:
            f.write('')


    def tearDown(self):
        UsersModel.TESTAPI_resetFixture()


    def testSingleGoodUser(self):
        self.assertEquals(UsersModel.add('user', 'password'), 1)
        users = UsersModel.objects.all()
        printToFile(users)
        assert len(users) == 1
        user = users[0]
        assert user.user == 'user'
        assert user.password == 'password'
        self.assertEquals(UsersModel.login('user','password'), 2)
        
    def testAddSingleBadUserName(self):
        self.assertEquals(UsersModel.add('', 'password'), ERR_BAD_USERNAME)
        assert len(UsersModel.objects.all())==0
    
    def testAddSingleBadPassword(self):
        pw = ''
        for _ in range(MAX_PASSWORD_LENGTH+1):
            pw = pw + 'x'
        self.assertEquals(UsersModel.add('user',pw), ERR_BAD_PASSWORD)
        assert len(UsersModel.objects.all())==0
    
    def testAddUserAlreadyExists(self):
        UsersModel.add('user','password')
        self.assertEquals(UsersModel.add('user','password2'), ERR_USER_EXISTS)
        self.assertEquals(len(UsersModel.objects.all()), 1)
        
    def testManyGoodUsers(self):
        numGoodUsers = 10
        for x in range(numGoodUsers):
            self.assertEquals(UsersModel.add('user%d' % x,'password%d' % x), SUCCESS)
        self.assertEquals(len(UsersModel.objects.all()), numGoodUsers)
    
    def testLoginGoodUser(self):
        UsersModel.add('user','password')
        numLogins = 10
        for login in range(1, numLogins):
            self.assertEquals(UsersModel.login('user', 'password'), login+1)
            
    def testLoginBadPassword(self):
        UsersModel.add('user','password')
        self.assertEqual(UsersModel.login('user','not_password'), ERR_BAD_CREDENTIALS)
        
    def testLoginBadUsername(self):
        UsersModel.add('user2','password')
        self.assertEquals(UsersModel.login('user', 'password'), ERR_BAD_CREDENTIALS)
        
    def testLoginMultipleTimesSingleUser(self):
        UsersModel.add('user','password')
        loginTimes = 10
        for x in range(2,loginTimes):
            self.assertEqual(UsersModel.login('user','password'), x)
    
    def testLoginMultipleTimesMultipleUser(self):
        UsersModel.add('user','password')
        UsersModel.add('user2','password')
        loginTimes = 20
        for x in range(2, loginTimes):
            self.assertEqual(UsersModel.login('user','password'), x)
            self.assertEqual(UsersModel.login('user2','password'), x)
