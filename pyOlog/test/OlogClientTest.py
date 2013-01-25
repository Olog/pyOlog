'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Jan 9, 2013

@author: shroffk
'''
import unittest
from pyOlog import OlogClient
from pyOlog.OlogDataTypes import Tag, Logbook, Property, LogEntry, Attachment
from datetime import datetime

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
        
    def testCreateProperty(self):
        '''
        Basic operations of creating, listing and deleting a Logbook object
        '''
#        client = OlogClient(url='https://localhost:8181/Olog', username='shroffk', password='1234')
#        testAttributes = {"attr":"test"}
#        testProperty = Property(name='testProperty', attributes=testAttributes)
#        client.createProperty(testProperty)
#        self.assertTrue(testProperty in client.listProperties(), 'failed to create the testProperty')
        '''Delete Property only deletes attributes in the service - will be fixed in the service'''
#        client.delete(propertyName='testProperty')
#        self.assertTrue(testProperty not in client.listProperties(), 'failed to cleanup the testProperty')
        
class TestLogEntryCreation(unittest.TestCase):
    
    def testCreateBasicEntry(self):
        client = OlogClient(url='https://localhost:8181/Olog', username='shroffk', password='1234')
        testLogbook = Logbook(name='testLogbook', owner='testOwner')
        client.createLogbook(testLogbook)
        text = 'test python log entry '+ datetime.now().isoformat(' ')
        testLog = LogEntry(text=text, owner='testOwner', logbooks=[testLogbook])
        client.log(logEntry=testLog)
        logEntries = client.find(text=testLog.getText())
        self.assertTrue(len(logEntries) == 1, 'Failed to create test log entry')
        client.delete(logEntryId=logEntries[0].getId())
        self.assertTrue(len(client.find(text=testLog.getText())) == 0, 'Failed to delete test log entry')
        client.delete(logbookName='testLogbook')
        self.assertTrue(testLogbook not in client.listLogbooks(), 'failed to cleanup the testLogbook')
        pass
    
    def testCreateEntryWithTag(self):
        client = OlogClient(url='https://localhost:8181/Olog', username='shroffk', password='1234')
        testLogbook = Logbook(name='testLogbook', owner='testOwner')
        client.createLogbook(testLogbook);
        testTag = Tag(name='testTag')
        client.createTag(testTag)        
        text = 'test python log entry with tag '+ datetime.now().isoformat(' ')
        testLog = LogEntry(text=text,
                           owner='testOwner',
                           logbooks=[testLogbook],
                           tags=[testTag])
        client.log(testLog)
        logEntries = client.find(text=testLog.getText())
        self.assertTrue(len(logEntries) == 1, 'Failed to create log Entry with Tag')
        self.assertTrue(testTag in logEntries[0].getTags(), 'testTag not attached to the testLogEntry')
        client.delete(logEntryId=logEntries[0].getId())
        self.assertTrue(len(client.find(text=testLog.getText())) == 0, 'Failed to delete log Entry with Tag')
        client.delete(logbookName=testLogbook.getName())
        self.assertTrue(testLogbook not in client.listLogbooks(), 'failed to cleanup the testLogbook')
        client.delete(tagName=testTag.getName())
        self.assertTrue(testTag not in client.listTags(), 'failed to cleanup the testTag')
        pass
    
    def testCreateEntryWithAttachments(self):
        client = OlogClient(url='https://localhost:8181/Olog', username='shroffk', password='1234')
        testLogbook = Logbook(name='testLogbook', owner='testOwner')
        client.createLogbook(testLogbook);
        text = 'test python log entry with attachment '+ datetime.now().isoformat(' ')
        testAttachment = Attachment(open('Desert.jpg', 'rb'))
        testLog = LogEntry(text=text,
                           owner='testOwner',
                           logbooks=[testLogbook],
                           attachments=[testAttachment]
                           )
        client.log(testLog)
        logEntries = client.find(text=text)
        self.assertEqual(len(logEntries), 1, 'Failed to create log entry with attachment')
        attachments = client.listAttachments(logEntryId=logEntries[0].getId())
        self.assertEqual(len(attachments), 1, 'Failed to create log entry with attachment');
        client.delete(logEntryId=logEntries[0].getId())       
        client.delete(logbookName=testLogbook.getName())
        self.assertTrue(testLogbook not in client.listLogbooks(), 'failed to cleanup the testLogbook')
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
