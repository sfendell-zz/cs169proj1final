"""
Unit tests for the models.py module.
This is just a sample. You should have more tests for your model (at least 10)
"""

import unittest
import sys
import models

class TestUsers(unittest.TestCase):
    """
    Unittests for the Users model class (a sample, incomplete)
    """
    def setUp(self):
        self.users = models.UsersModel ()
        self.users.reset ()

        
    def testAdd1(self):
        """
        Tests that adding a user works
        """
        self.assertEquals(models.SUCCESS, self.users.add("user1", "password"))

    def testAddExists(self):
        """
        Tests that adding a duplicate user name fails
        """
        self.assertEquals(models.SUCCESS, self.users.add("user1", "password"))
        self.assertEquals(models.ERR_USER_EXISTS, self.users.add("user1", "password"))

    def testAdd2(self):
        """
        Tests that adding two users works
        """
        self.assertEquals(models.SUCCESS, self.users.add("user1", "password"))
        self.assertEquals(models.SUCCESS, self.users.add("user2", "password"))

    def testAddEmptyUsername(self):
        """
        Tests that adding an user with empty username fails
        """
        self.assertEquals(models.ERR_BAD_USERNAME, self.users.add("", "password"))
        
        
    def testSingleGoodUser(self):
        self.assertEquals(self.users.add('user', 'password'), 1)
        users = self.users.objects.all()
        assert len(users) == 1
        user = users[0]
        assert user.user == 'user'
        assert user.password == 'password'
        self.assertEquals(self.users.login('user','password'), 2)
        
    
    def testAddSingleBadPassword(self):
        pw = ''
        for _ in range(models.MAX_PASSWORD_LENGTH+1):
            pw = pw + 'x'
        self.assertEquals(self.users.add('user',pw), models.ERR_BAD_PASSWORD)
        assert len(self.users.objects.all())==0
        
    def testManyGoodUsers(self):
        numGoodUsers = 10
        for x in range(numGoodUsers):
            self.assertEquals(self.users.add('user%d' % x,'password%d' % x), models.SUCCESS)
        self.assertEquals(len(self.users.objects.all()), numGoodUsers)
    
    def testLoginGoodUser(self):
        self.users.add('user','password')
        numLogins = 10
        for login in range(1, numLogins):
            self.assertEquals(self.users.login('user', 'password'), login+1)
            
    def testLoginBadPassword(self):
        self.users.add('user','password')
        self.assertEqual(self.users.login('user','not_password'), models.ERR_BAD_CREDENTIALS)
        
    def testLoginBadUsername(self):
        self.users.add('user2','password')
        self.assertEquals(self.users.login('user', 'password'), models.ERR_BAD_CREDENTIALS)
        

