'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Jan 8, 2013

@author: shroffk
'''
import unittest
from pyOlog import LogEntry, Tag, Logbook, Property, Attachment
    
class TestTag(unittest.TestCase):
    
    def testCreateTag(self):
        '''
        A Tag consists of a name and a state
        '''        
        tag1 = Tag(name='tagName')
        self.assertEqual(tag1.getName(), 'tagName', 'failed to create the tag correctly')
        '''Check equality which is based on name and state'''
        taga = Tag(name='testName', state='Active')
        tagb = Tag(name='testName', state='Active')
        self.assertEqual(taga, tagb, 'Failed equality condition')
        self.assertEqual([taga], [tagb], 'Failed equality condition')
        pass
    
class TestLogbook(unittest.TestCase):
    
    def testCreateLogbook(self):
        '''
        A Logbook consists of a name(required) and an owner(required)
        '''
        logbook = Logbook(name='logbookName', owner='logbookOwner')
        self.assertEqual(logbook.getName(), 'logbookName', 'Failed to create logbook')
        self.assertEqual(logbook.getOwner(), 'logbookOwner', 'Failed to create logbook')
        '''Check equality which is based on name and owner'''
        logbookA = Logbook(name='testName', owner='logbookOwner')
        logbookB = Logbook(name='testName', owner='logbookOwner')
        self.assertEqual(logbookA, logbookB, 'Failed equality condition')
        pass
    
class TestProperty(unittest.TestCase):
    
    def testCreateProperty(self):
        '''
        A Property consists of a name(required) and a set of attributes
        '''      
        attributes = {'attribute1':'attribute1Value', 'attribute2':'attribute2Value'}
        property1 = Property(name='propertyName', attributes=attributes)
        self.assertEqual(property1.getName(), 'propertyName', '')
        self.assertEqual(property1.getAttributes(), attributes , '')
        self.assertEqual(set(property1.getAttributeNames()), set(['attribute1', 'attribute2']), '')
        self.assertEqual(property1.getAttributeValue('attribute1'), 'attribute1Value', '')
        property2 = Property(name='propertyName', attributes={'attribute1':'attribute1Value', 'attribute2':'attribute2Value'})
        self.assertEqual(property1, property2, 'Failed equality condition')
        pass
  
class TestAttachment(unittest.TestCase):
    
    def testCreateAttachment(self):
        '''
        '''
        attachment = Attachment(file=open('Desert.jpg'))
        
        pass
      
class LogEntryTest(unittest.TestCase):
    
    def testCreateLog(self):
        '''
        '''
        tags = [ Tag(name='Timing'), Tag(name='Magnets') ]
        logbooks = [ Logbook(name='experiment', owner='controls') ]
        logEntry = LogEntry(text='Turning on LINAC', owner='controls', logbooks=logbooks, tags=tags)
        self.assertEqual(logEntry.getText(), 'Turning on LINAC', 'msg')
        self.assertEqual(logEntry.getOwner(), 'controls', 'msg')
        self.assertEqual(logEntry.getTags(), tags, 'msg')
#        self.assertTrue(logEntry.hasTag('Timing'), 'msg')
        self.assertEqual(logEntry.getLogbooks(), logbooks, 'msg')
#        self.assertTrue(logEntry.hasLogbook('experiment'), 'msg')
        pass
    
    def testCmp(self):
        tags = [ Tag(name='Timing'), Tag(name='Magnets') ]
        logbooks = [ Logbook(name='experiment', owner='controls') ]
        logEntry1 = LogEntry(text='Turning on LINAC', owner='controls', logbooks=logbooks, tags=tags, id=1234)
        logEntry2 = LogEntry(text='Turning on LINAC', owner='controls', logbooks=logbooks, tags=tags, id=1234)
        self.assertEqual(logEntry1, logEntry2, 'Failed LogEntry equality')
        self.assertIn(logEntry1, [logEntry2])
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
