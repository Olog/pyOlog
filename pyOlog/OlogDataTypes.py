'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Jan 10, 2013

@author: shroffk
'''

class LogEntry(object):
    '''
    A LogEntry consists of some Text description, an owner and an associated logbook
    It can optionally be associated with one or more logbooks and contain one or more tags, properties and attachments
    '''

    def __init__(self, text, owner, logbooks, tags=[], attachments=[], properties=[], id=None, createTime=None, modifyTime=None):
        '''
        Constructor for log Entry
        Simple LogEntry
        >> LogEntry('test log entry', 'controls', logbooks=[Logbook('commissioning', owner='controls')])
        
        Comprehensive logEntry
        >> LogEntry('test log entry', 'controls', 
                    logbooks=[Logbook('commissioning', owner='controls')],
                    tags=[Tag('TimingSystem')]
                    properties=[Property('Ticket', attributes={'Id':'1234','URL':'http://trac.nsls2.bnl.gov/trac/1234'}]
                    attachments=[Attachment(open('databrowser.plt'))]
                    )
        '''
        self.Text = str(text).strip();
        self.Owner = str(owner).strip();
        self.logbooks = logbooks
        self.tags = tags
        self.attachments = attachments
        self.properties = properties
        self.__id = id
        self.__createTime = createTime
        self.__modifytime = modifyTime
        
    def getId(self):
        return self.__id
    
    def getCreateTime(self):
        return self.__createTime
    
    def getModifyTime(self):
        return self.__modifytime
    
    def getText(self):
        return self.Text
    
    def getOwner(self):
        return self.Owner
    
    def getLogbooks(self):
        return self.logbooks
       
    def getTags(self):
        return self.tags
        
    def getAttachments(self):
        return self.attachments
    
    def getProperties(self):
        return self.properties
    
    def __cmp__(self, *arg, **kwargs):  
        if arg[0] == None:
            return 1 
        if self.__id:
            return cmp((self.__id),(arg[0].__id))
        else:
            raise Exception, 'Invalid LogEntry: id cannot be None'
        
        
class Logbook(object):
    '''
    A Logbook consist of an unique name and an owner, 
    logentries can be added to a logbook so long as the user either the owner
    or a member of the owner group
    '''

    def __init__(self, name, owner):
        '''
        Create a logbook
        >> Logbook('commissioning', 'controls')
        '''
        self.__Name = str(name).strip();
        self.__Owner = str(owner).strip();
        
    def getName(self):
        return self.__Name
    
    def getOwner(self):
        return self.__Owner
        
    def __cmp__(self, *arg, **kwargs):  
        if arg[0] == None:
            return 1      
        return cmp((self.__Name, self.__Owner), (arg[0].__Name, arg[0].__Owner))
           
class Tag(object):
    '''
    A Tag consists of a unique name, it is used to tag logEntries to enable querying and organizing log Entries
    '''

    def __init__(self, name, state="Active"):
        '''
        Create a Tag object
        >> Tag('TimingSystem')
        '''
        self.__Name = str(name).strip()
        self.__State = str(state).strip()
    
    def getName(self):
        return self.__Name
    
    def getState(self):
        return self.__State
    
    def __cmp__(self, *arg, **kwargs):  
        if arg[0] == None:
            return 1      
        return cmp((self.__Name, self.__State), (arg[0].__Name, arg[0].__State))
    
class Attachment(object):
    '''
    A Attachment, a file associated with the log entry
    TODO this is not thread safe    
    '''
    
    def __init__(self, file):
        '''
        Create Attachment 
        >> Attachment(file=open('/home/usr/databrowser.plt')
        >> Attachment(file=open('test.jpg','rb')
        '''
        self.__file=file
        
    def getFile(self):
        return self.__file

class Property(object):
    '''
    A property consists of a unique name and a set of attributes consisting of key value pairs   
    '''
    
    def __init__(self, name, attributes=None):
        '''
        Create a property with a unique name and attributes
        >> Property('Ticket', attributes={'Id':'1234','URL':'http://trac.nsls2.bnl.gov/trac/1234'}
        >> Property('Scan', attributes={'Number':'run-1234', 'script':'scan_20130117.py'}
        '''
        self.__Name = str(name).strip()
        self.Attributes = attributes
        
    def getName(self):
        return self.__Name
    
    def getAttributes(self):
        return self.Attributes;
    
    def getAttributeNames(self):
        return self.Attributes.keys()
    
    def getAttributeValue(self, attributeName):
        return self.Attributes.get(attributeName)
    
    def __cmp__(self, *arg, **kwargs):  
        if arg[0] == None:
            return 1      
        return cmp((self.__Name, set(self.Attributes)), (arg[0].__Name, set(arg[0].Attributes)))
    
