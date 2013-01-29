'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Jan 9, 2013

@author: shroffk
'''
import unittest
from pyOlog import OlogClient
from pyOlog import Tag, Logbook, Property, LogEntry, Attachment
from datetime import datetime
import time

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
        
    def CreateProperty(self):
        '''
        Basic operations of creating, listing and deleting a Logbook object
        '''
        client = OlogClient(url='https://localhost:8181/Olog', username='shroffk', password='1234')
        testAttributes = {"attr":"test"}
        testProperty = Property(name='testProperty32', attributes=testAttributes)
        client.createProperty(testProperty)
        self.assertTrue(testProperty in client.listProperties(), 'failed to create the testProperty')
        '''Delete Property only deletes attributes in the service - will be fixed in the service'''
        client.delete(propertyName='testProperty')
        self.assertTrue(testProperty not in client.listProperties(), 'failed to cleanup the testProperty')
        
class TestLogEntryCreation(unittest.TestCase):
    
    def testCreateBasicEntry(self):
        client = OlogClient(url='https://localhost:8181/Olog', username='shroffk', password='1234')
        testLogbook = Logbook(name='testLogbook', owner='testOwner')
        client.createLogbook(testLogbook)
        text = 'test python log entry ' + datetime.now().isoformat(' ')
        testLog = LogEntry(text=text,
                           owner='testOwner',
                           logbooks=[testLogbook])
        client.log(logEntry=testLog)
        logEntries = client.find(search=testLog.getText())
        self.assertTrue(len(logEntries) == 1, 'Failed to create test log entry')
        client.delete(logEntryId=logEntries[0].getId())
        self.assertTrue(len(client.find(search=testLog.getText())) == 0, 'Failed to delete test log entry')
        client.delete(logbookName='testLogbook')
        self.assertTrue(testLogbook not in client.listLogbooks(), 'failed to cleanup the testLogbook')
        pass
    
    def testCreateEntryWithTag(self):
        client = OlogClient(url='https://localhost:8181/Olog', username='shroffk', password='1234')
        testLogbook = Logbook(name='testLogbook', owner='testOwner')
        client.createLogbook(testLogbook);
        testTag = Tag(name='testTag')
        client.createTag(testTag)        
        text = 'test python log entry with tag ' + datetime.now().isoformat(' ')
        testLog = LogEntry(text=text,
                           owner='testOwner',
                           logbooks=[testLogbook],
                           tags=[testTag])
        client.log(testLog)
        logEntries = client.find(search=testLog.getText())
        self.assertTrue(len(logEntries) == 1, 'Failed to create log Entry with Tag')
        self.assertTrue(testTag in logEntries[0].getTags(), 'testTag not attached to the testLogEntry1')
        '''cleanup'''
        client.delete(logEntryId=logEntries[0].getId())
        self.assertTrue(len(client.find(search=testLog.getText())) == 0, 'Failed to delete log Entry with Tag')
        client.delete(logbookName=testLogbook.getName())
        self.assertTrue(testLogbook not in client.listLogbooks(), 'failed to cleanup the testLogbook')
        client.delete(tagName=testTag.getName())
        self.assertTrue(testTag not in client.listTags(), 'failed to cleanup the testTag')
        pass
    
    def testCreateEntryWithAttachments(self):
        client = OlogClient(url='https://localhost:8181/Olog', username='shroffk', password='1234')
        testLogbook = Logbook(name='testLogbook', owner='testOwner')
        client.createLogbook(testLogbook);
        text = 'test python log entry with attachments ' + datetime.now().isoformat(' ')
        testImageAttachment = Attachment(open('Desert.jpg', 'rb'))
        testTextAttachment = Attachment(open('debug.log','rb'))
        testLog = LogEntry(text=text,
                           owner='testOwner',
                           logbooks=[testLogbook],
                           attachments=[testImageAttachment, testTextAttachment]
                           )
        client.log(testLog)
        logEntries = client.find(search=text)
        self.assertEqual(len(logEntries), 1, 'Failed to create log entry with attachment')
        attachments = client.listAttachments(logEntryId=logEntries[0].getId())
        self.assertEqual(len(attachments), 2, 'Failed to create log entry with attachment');
        for attachment in attachments:
            if attachment.getFile().name.endswith('.log'):
                print attachment.getFile().readline()
                print attachment.getFile().fileno(), open('debug.log','rb').fileno()      
        client.delete(logEntryId=logEntries[0].getId()) 
        self.assertEqual(len(client.find(search=text)), 0, 'Failed to cleanup log entry with attachment')      
        client.delete(logbookName=testLogbook.getName())
        self.assertTrue(testLogbook not in client.listLogbooks(), 'failed to cleanup the testLogbook')
        pass
    
    def testCreateEntryWithProperties(self):
        client = OlogClient(url='https://localhost:8181/Olog', username='shroffk', password='1234')
        testLogbook = Logbook(name='testLogbook', owner='testOwner')
        client.createLogbook(testLogbook);
        testProperty = Property(name='testLogProperty', attributes={'id':None, 'url':None})
#        client.createProperty(testProperty)
        text = 'test python log entry with attachment ' + datetime.now().isoformat(' ')
        property = Property(name='testLogProperty', attributes={'id':'prop1234', 'url':'www.bnl.gov'})
        testLog = LogEntry(text=text,
                           owner='testOwner',
                           logbooks=[testLogbook],
                           properties=[property]
                           )
        client.log(testLog)
        logEntries = client.find(search=text)
        self.assertEqual(len(logEntries), 1, 'Failed to create log entry with property')
        properties = logEntries[0].getProperties()
        self.assertIn(property, properties, 'TestLogEntry does not contain property ' + property.getName())
        '''Cleanup'''
        client.delete(logEntryId=logEntries[0].getId()) 
        self.assertEqual(len(client.find(search=text)), 0, 'Failed to cleanup log entry with property') 
        client.delete(logbookName=testLogbook.getName())
        self.assertTrue(testLogbook not in client.listLogbooks(), 'failed to cleanup the ' + testLogbook.getName())
        pass

class LogEntrySearchTest(unittest.TestCase):
    
    def setUp(self):
        self.client = client = OlogClient(url='https://localhost:8181/Olog', username='shroffk', password='1234')
        self.text = 'test python log entry with attachment ' + datetime.now().isoformat(' ')
        self.testAttachment = Attachment(open('Desert.jpg', 'rb'))
        self.testLogbook = Logbook(name='testLogbook', owner='testOwner')
        self.client.createLogbook(self.testLogbook);
        self.testTag = Tag(name='testTag') 
        self.client.createTag(self.testTag)               
        self.testProperty = Property(name='testLogProperty', attributes={'id':'testSearchId', 'url':'www.bnl.gov'})
        self.t1 = str(time.time()).split('.')[0]
        client.log(LogEntry(text=self.text,
                           owner='testOwner',
                           logbooks=[self.testLogbook],
                           tags=[self.testTag],
                           attachments=[self.testAttachment],
                           properties=[self.testProperty]))
        self.t2 = str(time.time()).split('.')[0]
        client.log(LogEntry(text=self.text + ' - entry2',
                           owner='testOwner',
                           logbooks=[self.testLogbook]))
        self.t3 = str(time.time()).split('.')[0]
        self.testLogEntry1 = client.find(search=self.text)[0]
        self.testLogEntry2 = client.find(search=self.text + ' - entry2')[0]
        pass

    def tearDown(self):
        self.client.delete(logbookName=self.testLogbook.getName())
        self.client.delete(tagName=self.testTag.getName())
        self.client.delete(logEntryId=self.testLogEntry1.getId())
        self.client.delete(logEntryId=self.testLogEntry2.getId())
        pass
    
    def testSearchByText(self):
        self.assertIn(self.testLogEntry1, self.client.find(search=self.text), 'Failed to search by text')
        pass
    
    def testSearchByTag(self):
        self.assertIn(self.testLogEntry1, self.client.find(tag=self.testTag.getName()), 'Failed to search by Tag')
        pass
    
    def testSearchByLogbook(self):
        self.assertIn(self.testLogEntry1, self.client.find(logbook=self.testLogbook.getName()), 'Failed to search by logbook')
        pass
    
    def testSearchByProperty(self):
        self.assertIn(self.testLogEntry1, self.client.find(property=self.testProperty.getName()), 'Failed to search by property')
        pass
    
    def testSearchByTime(self):
        self.assertIn(self.testLogEntry1, self.client.find(start=self.t1, end=self.t2), 'Failed to search by time')
        logEntries = self.client.find(start=self.t1, end=self.t3)
        self.assertIn(self.testLogEntry1, logEntries, 'Failed to search by time')
        self.assertIn(self.testLogEntry2, logEntries, 'Failed to search by time')
        pass
    
    def testSearchByMultipleParamerters(self):
        self.assertIn(self.testLogEntry1, self.client.find(search=self.text, tag=self.testTag.getName(), logbook=self.testLogbook.getName()))
        logEntries =  self.client.find(start=self.t1, end=self.t3, tag=self.testTag.getName())
        self.assertIn(self.testLogEntry1, logEntries, 'Failed to search by time and tag')
        self.assertNotIn(self.testLogEntry2, logEntries, 'Failed to correctly search by time and tag')
        pass
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
