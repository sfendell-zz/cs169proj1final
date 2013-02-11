'''
Created on Feb 11, 2013

@author: samuelfendell
'''
import testLib



        
class TestAddUser(testLib.RestTestCase):
    """Test adding users"""
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testAdd1(self):
        respData = self.makeRequest("/users/add/", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)

    def testAddBadUser(self):
        respData = self.makeRequest("/users/add/", method="POST", data={ 'user' : '', 'password' : 'password'})
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_USERNAME)
    
    def testAddBadPassword(self):
        badPw = ''
        for _ in range(1000):
            badPw = badPw + '*'
        respData = self.makeRequest("/users/add/", method = "POST", data={'user': 'user', 'password': badPw})
    
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_PASSWORD)