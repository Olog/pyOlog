'''
Created on Jan 10, 2013

@author: shroffk
'''
import requests
from json import JSONEncoder,JSONDecoder, loads
from copy import copy
from OlogDataTypes import *
import json

class OlogClient(object):
    '''
    classdocs
    '''
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}

    def __init__(self, url='https://localhost:8181/Olog/resources', username=None,password=None):
        '''
        Constructor
        '''
        try:     
            self.__url = url   
            resp = requests.get(self.__url+'/tags', verify=False, headers=self.__jsonheader)
        except:
            raise
        
class TagDecoder(JSONDecoder):
    
    def __init__(self):
        json.JSONDecoder.__init__(self,object_hook=self.dict_to_tag)
        
    def dict_to_tag(self, d):
        if d:
            d = {}
            name = d.pop('name')
            state = d.pop('state')
            return Tag(name=name,state=state)
        else:
            return None