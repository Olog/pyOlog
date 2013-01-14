'''
Created on Jan 10, 2013

@author: shroffk
'''

class LogEntry(object):
    '''
    classdocs
    '''


    def __init__(self, text, owner, logbooks, tags=None, attachments=None, properties=None):
        '''
        Constructor
        '''
        self.__Text = str(text).strip();
        self.__Owner = str(owner).strip();
        self.logbooks = logbooks
        self.tags = tags
        self.attachments = attachments
        self.properties = properties
        
    def getText(self):
        return self.__Text
    
    def getOwner(self):
        return self.__Owner
    
    def getLogbooks(self):
        return self.logbooks
       
    def getTags(self):
        return self.tags
        
    def getAttachments(self):
        return self.attachments
    
    def getProperties(self):
        return self.properties
        
        
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
    
           
class Tag(object):
    '''
    classdocs
    '''


    def __init__(self, name, state=None):
        '''
        Constructor
        '''
        self.__Name = str(name).strip();
    
    def getName(self):
        return self.__Name
    
class Property(object):
    '''
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
    