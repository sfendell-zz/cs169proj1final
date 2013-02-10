"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *
import os
base_dir = os.path.dirname(__file__)


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
            self.assertEquals(UsersModel.login('user', 'password'), login)