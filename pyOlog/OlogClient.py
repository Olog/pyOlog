'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Jan 10, 2013

@author: shroffk
'''
import requests
from json import JSONEncoder, JSONDecoder
from OlogDataTypes import LogEntry, Logbook, Tag, Property, Attachment
import json
from requests import auth
import logging
from urllib import urlencode
from collections import OrderedDict

class OlogClient(object):
    '''
    classdocs
    '''
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}
    __logsResource = '/resources/logs'
    __propertiesResource = '/resources/properties'
    __tagsResource = '/resources/tags'
    __logbooksResource = '/resources/logbooks'
    __attachmentResource ='/resources/attachments'

    def __init__(self, url='https://localhost:8181/Olog', username=None, password=None):
        '''
        Constructor
        '''
        try:     
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.DEBUG)
            self.__url = url
            self.__username = username
            self.__password = password
            if username and password:
                self.__auth = auth.HTTPBasicAuth(username, password)
            else:
                self.__auth = None
            resp = requests.get(self.__url + self.__tagsResource, verify=False, headers=self.__jsonheader)
        except:
            raise
    
    def log(self, logEntry):
        '''
        create a logEntry
        '''
        resp = requests.post(self.__url + self.__logsResource,
                     data=LogEntryEncoder().encode(logEntry),
                     verify=False,
                     headers=self.__jsonheader,
                     auth=self.__auth)
        resp.raise_for_status()
        id = LogEntryDecoder().dictToLogEntry(resp.json()[0]).getId()
        '''Attachments'''
        for attachment in logEntry.getAttachments():
            resp = requests.post('https://localhost:8181/Olog/resources/attachments/'+str(id), 
                                  verify=False, 
                                  auth=self.__auth, 
                                  files={'file':attachment.getFile()}
                                  )
            resp.raise_for_status()
            
            
    
    def createLogbook(self, logbook):
        '''
        Create Logbook
        '''
        requests.put(self.__url + self.__logbooksResource + '/' + logbook.getName(),
                     data=LogbookEncoder().encode(logbook),
                     verify=False,
                     headers=self.__jsonheader,
                     auth=self.__auth).raise_for_status()
        
        
    def createTag(self, tag):
        '''
        Create Tag
        '''
        url = self.__url + self.__tagsResource + '/' + tag.getName()
        requests.put(url,
                     data=TagEncoder().encode(tag),
                     verify=False,
                     headers=self.__jsonheader,
                     auth=self.__auth).raise_for_status()
        
    def createProperty(self, property):
        '''
        Create Property
        '''
        url = self.__url + self.__propertiesResource + '/' + property.getName()
        p = PropertyEncoder().encode(property)
        requests.put(url,
                     data=PropertyEncoder().encode(property),
                     verify=False,
                     headers=self.__jsonheader,
                     auth=self.__auth).raise_for_status()
        
    def find(self, **kwds):
        '''
        Search for logEntries based on one or many search criteria
        >> find(search='*Timing*')
        find logentries with the text Timing in the description
        
        >> find(tag='magnets')
        find log entries with the a tag named 'magnets'
        
        >> find(logbook='controls')
        find log entries in the logbook named 'controls'
        
        >> find(property='context')
        find log entires with property named 'context'
        
        >> find(start=str(time.time() - 3600)
        find the log entries made in the last hour
        >> find(start=123243434, end=123244434)
        find all the log entries made between the epoc times 123243434 and 123244434
        
        Searching using multiple criteria
        >>find(logbook='contorls', tag='magnets')
        find all the log entries in logbook 'controls' AND with tag named 'magnets'
        '''
        #search = '*' + text + '*'
        query_string = self.__url + self.__logsResource + '?' + urlencode(OrderedDict(kwds))
        resp = requests.get(query_string,
                            verify=False,
                            headers=self.__jsonheader,
                            auth=self.__auth
                            )
        resp.raise_for_status()
        logs = []
        for jsonLogEntry in resp.json():            
            logs.append(LogEntryDecoder().dictToLogEntry(jsonLogEntry))
        return logs
    
    def listAttachments(self, logEntryId):
        '''
        Search for attachments on logentry _id_
        '''
        resp = requests.get(self.__url+self.__attachmentResource+'/'+str(logEntryId),
                         verify=False,
                         headers=self.__jsonheader)
        resp.raise_for_status()
        attachments = []
        for jsonAttachment in resp.json().pop('attachment'):
            fileName = jsonAttachment.pop('fileName')
            print self.__url+self.__attachmentResource+'/'+str(logEntryId)+'/'+fileName
            f = requests.get(self.__url+
                             self.__attachmentResource+'/'+
                             str(logEntryId)+'/'+
                             fileName,
                             verify=False)
            test = open('tmp'+fileName, 'wb')
            test.write(f.content)
            attachments.append(Attachment(file=test))
        return attachments           
    
    def listTags(self):
        '''
        List all tags.
        '''
        resp = requests.get(self.__url + self.__tagsResource,
                            verify=False,
                            headers=self.__jsonheader,
                            auth=self.__auth)
        resp.raise_for_status()
        tags = []
        for jsonTag in resp.json().pop('tag'):
            tags.append(TagDecoder().dictToTag(jsonTag))
        return tags
    
    def listLogbooks(self):
        '''
        List all logbooks
        '''
        resp = requests.get(self.__url + self.__logbooksResource,
                            verify=False,
                            headers=self.__jsonheader,
                            auth=self.__auth)
        resp.raise_for_status()
        logbooks = []
        for jsonLogbook in resp.json().pop('logbook'):
            logbooks.append(LogbookDecoder().dictToLogbook(jsonLogbook))
        return logbooks
    
    def listProperties(self):
        '''
        List all Properties and their attributes
        '''
        resp = requests.get(self.__url + self.__propertiesResource,
                            verify=False,
                            headers=self.__jsonheader,
                            auth=self.__auth)
        resp.raise_for_status()
        properties = []
        for jsonProperty in resp.json().pop('property'):
            properties.append(PropertyDecoder().dictToProperty(jsonProperty))
        return properties
            
                        
    def delete(self, **kwds):
        '''
        Method to delete a logEntry, logbook, property, tag
        delete(logEntryId = int)
        >>> delete(logEntryId=1234)
        
        delete(logbookName = String)
        >>> delete(logbookName = 'logbookName')
        
        delete(tagName = String)
        >>> delete(tagName = 'myTag')
        # tagName = tag name of the tag to be deleted (it will be removed from all logEntries)
        
        delete(propertyName = String)
        >>> delete(propertyName = 'position')
        # propertyName = property name of property to be deleted (it will be removed from all logEntries)
        '''
        if len(kwds) == 1:
            self.__handleSingleDeleteParameter(**kwds)
        else:
            raise Exception, 'incorrect usage: Delete a single Logbook/tag/property'
        
        
    def __handleSingleDeleteParameter(self, **kwds):
        if 'logbookName' in kwds:
            requests.delete(self.__url + self.__logbooksResource + '/' + kwds['logbookName'].strip(),
                        verify=False,
                        headers=self.__jsonheader,
                        auth=self.__auth).raise_for_status()
            pass
        elif 'tagName' in kwds:
            requests.delete(self.__url + self.__tagsResource + '/' + kwds['tagName'].strip(),
                        verify=False,
                        headers=self.__jsonheader,
                        auth=self.__auth).raise_for_status()
            pass
        elif 'propertyName' in kwds:
            requests.delete(self.__url + self.__propertiesResource + '/' + kwds['propertyName'].strip(),
                        verify=False,
                        headers=self.__jsonheader,
                        auth=self.__auth).raise_for_status()
            pass
        elif 'logEntryId' in kwds:
            requests.delete(self.__url + self.__logsResource + '/' + str(kwds['logEntryId']).strip(),
                            verify=False,
                            headers=self.__jsonheader,
                            auth=self.__auth).raise_for_status()
            pass
        else:
            raise Exception, ' unkown key, use logEntryId, logbookName, tagName or propertyName'

class PropertyEncoder(JSONEncoder):
    
    def default(self, obj):
        if isinstance(obj, Property):
            test = {}
            for key in obj.getAttributes():
                test[str(key)] = str(obj.getAttributeValue(key))
            prop = OrderedDict()
            prop["name"] = obj.getName()
            prop["attributes"] = test
            return prop
        return json.JSONEncoder.default(self, obj)

class PropertyDecoder(JSONDecoder):
    
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dictToProperty)
        
    def dictToProperty(self, d):
        if d:
            return Property(name=d.pop('name'), attributes=d.pop('attributes'))
    
class LogbookEncoder(JSONEncoder):
    
    def default(self, obj):
        if isinstance(obj, Logbook):
            return {"name":obj.getName(), "owner":obj.getOwner()}
        return json.JSONEncoder.default(self, obj)

class LogbookDecoder(JSONDecoder):
    
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dictToLogbook)
        
    def dictToLogbook(self, d):
        if d:
            return Logbook(name=d.pop('name'), owner=d.pop('owner'))
        else:
            return None
        
class TagEncoder(JSONEncoder):
       
    def default(self, obj):
        if isinstance(obj, Tag):
            return {"state": obj.getState(), "name": obj.getName()}
        return json.JSONEncoder.default(self, obj)
                
class TagDecoder(JSONDecoder):
    
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dictToTag)
        
    def dictToTag(self, d):
        if d:
            return Tag(name=d.pop('name'), state=d.pop('state'))
        else:
            return None
        
class LogEntryEncoder(JSONEncoder):
    
    def default(self, obj):
        if isinstance(obj, LogEntry):
            logbooks = []
            for logbook in obj.getLogbooks():
                logbooks.append(LogbookEncoder().default(logbook))
            tags = []
            for tag in obj.getTags():
                tags.append(TagEncoder().default(tag))
            properties = []
            for property in obj.getProperties():
                properties.append(PropertyEncoder().default(property))
            return [{"description":obj.getText(),
                   "owner":obj.getOwner(),
                   "level":"Info",
                   "logbooks":logbooks,
                   "tags":tags,
                   "properties":properties}]
        return json.JSONEncoder.default(self, obj)

class LogEntryDecoder(JSONDecoder):
    
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dictToLogEntry)
        
    def dictToLogEntry(self, d):
        if d:
            return LogEntry(text=d.pop('description'),
                            owner=d.pop('owner'),
                            logbooks=[LogbookDecoder().dictToLogbook(logbook) for logbook in d.pop('logbooks')],
                            tags=[TagDecoder().dictToTag(tag) for tag in d.pop('tags')],
                            properties=[PropertyDecoder().dictToProperty(property) for property in d.pop('properties')],
                            id=d.pop('id'),
                            createTime=d.pop('createdDate'),
                            modifyTime=d.pop('modifiedDate'))
        else:
            return None
