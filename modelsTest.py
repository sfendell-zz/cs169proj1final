'''
Created on Feb 8, 2013

@author: samuelfendell
'''
from django.utils import unittest
from cs169proj1.models import UsersModel


class Test(unittest.TestCase):


    def runTest(self):
        self.testSingleGoodUser()

    def setUp(self):
        pass


    def tearDown(self):
        UsersModel.TESTAPI_resetFixture()


    def testSingleGoodUser(self):
        self.assertEquals(UsersModel.add('user', 'password'), 1)
        users = UsersModel.objects()
        assert len(users) == 1
        user = users[0]
        assert user.name == 'user'
        assert user.password == 'password'
        self.assertEquals(UsersModel.login('user','password'), 2)
        
    def testSingleBadUser(self):
        self.assertEquals(UsersModel.add(''))