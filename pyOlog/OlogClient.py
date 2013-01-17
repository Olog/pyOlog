'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Jan 10, 2013

@author: shroffk
'''
import requests
from json import JSONEncoder, JSONDecoder, loads
from copy import copy
from OlogDataTypes import *
from StringIO import StringIO
import json
from PIL import Image
from StringIO import StringIO
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
        
    def createTag(self, tag):
        '''
        Create a Tag in the service
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
        List all the tags that exist.
        '''
        resp = requests.get(self.__url + self.__tagsResource,
                           verify=False,
                           headers=self.__jsonheader,
                           auth=self.__auth)
        resp.raise_for_status()
        tags = []
        for tag in resp.json().pop('tag'):
            tags.append(TagDecoder().dict_to_tag(tag))
        return tags
    
    def deletTag(self, tagName):
        '''
        delete the tag identified by tagName
        '''
        requests.delete(self.__url + self.__tagsResource + '/' + tagName,
                        verify=False,
                        headers=self.__jsonheader,
                        auth=self.__auth).raise_for_status()

class TagEncoder(JSONEncoder):
       
    def default(self, obj):
        if isinstance(obj, Tag):
            return {"state": obj.getState(), "name": obj.getName()}
        return json.JSONEncoder.default(self, obj)
                
class TagDecoder(JSONDecoder):
    
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_tag)
        
    def dict_to_tag(self, d):
        if d:
            return Tag(name=d.pop('name'), state=d.pop('state'))
        else:
            return None
