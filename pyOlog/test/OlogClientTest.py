'''
Created on Jan 9, 2013

@author: shroffk
'''
import unittest
from pyOlog import OlogClient

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

class TestCreateClientTest(unittest.TestCase):
    
    def testCreateClient(self):
        client = OlogClient(url='http://localhost:8080/Olog/resources')
        self.assertIsNotNone(client, 'Failed to create olog client')
        client = OlogClient(url='https://localhost:8181/Olog/resources')
        self.assertIsNotNone(client, 'Failed ti create olog client')
        pass
    
class LogEntryCreationTest(unittest.TestCase):
    
    def createBasicEntry(self):
        pass
    
    def createEntryWithAttachments(self):
        pass
    
    def createEntryWithProperties(self):
        pass

class LogEntrySearchTest(unittest.TestCase):
    
    def searchByText(self):
        pass
    
    def searchByTag(self):
        pass
    
    def searchByLogbook(self):
        pass
    
    def searchByProperty(self):
        pass
    
    def searchByTime(self):
        pass
    
    def searchByMultipleParamerters(self):
        pass
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()