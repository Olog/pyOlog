'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Jan 9, 2013

@author: shroffk
'''
import unittest
from pyOlog import OlogClient
from pyOlog.OlogDataTypes import Tag, Logbook

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

class TestCreateClient(unittest.TestCase):
    
    def testCreateClient(self):
        '''
        Simple test to create a ologClient
        '''
        client = OlogClient(url='http://localhost:8080/Olog')
        self.assertIsNotNone(client, 'Failed to create olog client')
        client = OlogClient(url='https://localhost:8181/Olog')
        self.assertIsNotNone(client, 'Failed to create olog client')
        pass

class TestCreate(unittest.TestCase):
    
    def testCreateTag(self):
        '''
        Basic operations of creating, listing and deleting a Tag object
        '''
        client = OlogClient(url='https://localhost:8181/Olog', username='shroffk', password='1234')
        testTag = Tag(name='testTag', state="Active")
        client.createTag(testTag)
        self.assertTrue(testTag in client.listTags(), 'failed to create the testTag')
        client.delete(tagName='testTag')
        self.assertTrue(testTag not in client.listTags(), 'failed to cleanup the testTag')
        
    def testCreateLogbook(self):
        '''
        Basic operations of creating, listing and deleting a Logbook object
        '''
        client = OlogClient(url='https://localhost:8181/Olog', username='shroffk', password='1234')
        testLogbook = Logbook(name='testLogbook', owner='testOwner')
        client.createLogbook(testLogbook)
        self.assertTrue(testLogbook in client.listLogbooks(), 'failed to create the testLogbook')
        client.delete(logbookName='testLogbook')
        self.assertTrue(testLogbook not in client.listLogbooks(), 'failed to cleanup the testLogbook')        
        
    
class TestLogEntryCreation(unittest.TestCase):
    
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
