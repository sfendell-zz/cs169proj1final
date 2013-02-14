'''
Created on Feb 11, 2013

@author: samuelfendell
'''
import testLib

class TestUser(testLib.RestTestCase):
    '''
    Just making sure all subclasses have assertResponse
    '''
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

        
class TestAddUserAdditional(TestUser):
    """More Tests adding users"""

    def testAddBadUser(self):
        respData = self.makeRequest("/users/add/", method="POST", data={ 'user' : '', 'password' : 'password'})
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_USERNAME)
    
    def testAddBadPassword(self):
        badPw = ''
        for _ in range(1000):
            badPw = badPw + '*'
        respData = self.makeRequest("/users/add/", method = "POST", data={'user': 'user', 'password': badPw})
    
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_PASSWORD)
    
class TestLoginUser(TestUser):
    def testSingleGoodLogin(self):
        '''
        Tests that a single good login works.
        '''
        self.makeRequest("/users/add/", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        respData = self.makeRequest('/users/login/', method="POST", data = {'user' : 'user1', 'password' : 'password'})
        self.assertResponse(respData, count=2)
    
    def testSingleBadLoginPassword(self):
        '''
        Tests that a single login with a bad password doesn't work.
        ''' 
        self.makeRequest("/users/add/", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        respData = self.makeRequest("/users/login/", method="POST", data = { 'user' : 'user1', 'password' : 'notpassword'} )
        self.assertResponse(respData, count=None, errCode=testLib.RestTestCase.ERR_BAD_CREDENTIALS)

    def testSingleBadLoginUsername(self):
        '''
        Tests that a single login with a bad username doesn't work.
        '''
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        respData = self.makeRequest("/users/login/", method="POST", data = { 'user' : 'notuser', 'password' : 'password'} )
        self.assertResponse(respData, count=None, errCode=testLib.RestTestCase.ERR_BAD_CREDENTIALS)

    def testLongUsername(self):
        user = 'ab' * 128
        addRespData = self.makeRequest("/users/add", method="POST", data = {'user' : user, 'password' : 'password'})
        self.assertResponse(addRespData, count=None, errCode = testLib.RestTestCase.ERR_BAD_USERNAME)
        loginRespData = self.makeRequest("/users/login", method="POST", data = {'user' : user, 'password' : 'password'})
        self.assertResponse(loginRespData, count=None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)

    def testBadAndGoodLogin(self):
        '''
        Tests that a single good login works after a bad one fails.
        '''
        
        respData = self.makeRequest("/users/add/", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count=1)
        
        respData = self.makeRequest("/users/login/", method="POST", data = { 'user' : 'user1', 'password' : 'notpassword'} )
        self.assertResponse(respData, count=None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)
        
        respData = self.makeRequest("/users/login/", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count=2)

    