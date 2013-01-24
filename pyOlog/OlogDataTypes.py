'''
Created on Jan 10, 2013

@author: shroffk
'''
import exceptions

class LogEntry(object):
    '''
    classdocs
    '''

    def __init__(self, text, owner, logbooks, tags=[], attachments=[], properties=[], id=None, createTime=None, modifyTime=None):
        '''
        Constructor
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
    classdocs
    '''

    def __init__(self, name, owner):
        '''
        Constructor
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
    A Tag consists of a unique name, it is used to tag logEntries to enable quering and organization 
    '''


    def __init__(self, name, state="Active"):
        '''
        Constructor
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
    '''
    
    def __init__(self, file):
        self.__file=file
        
    def getFile(self):
        return self.__file

class Property(object):
    '''
    A property consists of a unique name and a set of attributes consisting of key value pairs
    e.g.
    Property('Ticket', attributes={'Id':'1234','URL':'http://trac.nsls2.bnl.gov/trac/1234'}
    Property('Scan', attributes={'Number':'run-1234', 'script':'scan_20130117.py'}
    '''
    
    def __init__(self, name, attributes=None):
        '''
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
    
