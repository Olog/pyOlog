'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Jan 10, 2013

@author: shroffk
'''
import requests
from json import JSONEncoder, JSONDecoder
from OlogDataTypes import *
import json
from requests import auth

class OlogClient(object):
    '''
    classdocs
    '''
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}
    __logsResource = '/resources/logs'
    __propertiesResource = '/resources/properties'
    __tagsResource = '/resources/tags'
    __logbooksResource = '/resources/logbooks'

    def __init__(self, url='https://localhost:8181/Olog', username=None, password=None):
        '''
        Constructor
        '''
        try:     
            self.__url = url
            self.__username = username
            self.__password = password
            if username and password:
                self.__auth = auth.HTTPBasicAuth(username, password)
            else:
                self.__auth = None
            resp = requests.get(self.__url + self.__tagsResource, verify=False, headers=self.__jsonheader)
            '''
            try:
                f = requests.get('https://localhost:8181/Olog/resources/attachments/3233/trend.png', verify=False, headers=self.__jsonheader)
                print 'hello :', f
                test = open('plot4.png', 'wb')
                test.write(f.content)
                file = {'file':open('redder.jpg', 'rb')}
                imageFile = {'file' : Image.open('trend.png', 'r')}
                header = {'content-type':'image/png'}
                r = requests.post('https://localhost:8181/Olog/resources/attachments/3233', 
                                  verify=False, 
                                  auth=auth.HTTPBasicAuth('shroffk', '1234'), 
                                  files=file
                                  )
                print r                
            except:
                print 'error'
                raise
#            print resp.json()
#            print requests.get(self.__url+'/tags/Bumps', verify=False, headers=self.__jsonheader).json()
'''
        except:
            raise
    
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
        resp = requests.put(url,
                            data=TagEncoder().encode(tag),
                            verify=False,
                            headers=self.__jsonheader,
                            auth=self.__auth)
        resp.raise_for_status()
        
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
                        
    def delete(self, **kwds):
        '''
        Method to delete a logbook, property, tag
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
        else:
            raise Exception, ' unkown key, use logbookName, tagName or proprtyName'

class LogbookEncoder(JSONEncoder):
    
    def default(self, obj):
        if isinstance(obj, Logbook):
            return {"name":obj.getName(), "owner":obj.getOwner()}
        return json.JSONDecoder.decode(self, obj)

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
