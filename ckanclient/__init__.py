__version__ = '0.1a'
__description__ = 'CKAN client software.'
__long_description__ = \
''' The CKAN client software may be used to make requests on the Comprehensive
Knowledge Archive Network (CKAN) REST API.

The simplest way to make CKAN requests is:

    import ckanclient

    # Instantiate the CKAN client.
    ckan = ckanclient.CkanClient(api_key=my_key)
    
    # Get the package list.
    ckan.package_register_get()
    package_list = ckan.last_message
    print package_list

    # Register details of a new package.
    package_entity = {
        'name': my_package_name,
        'url': my_package_url,
        'download_url': my_package_download_url,
    }
    ckan.package_entity_post(package_entity)

    # Get the details of a package.
    ckan.package_entity_get(package_name)
    package_entity = ckan.last_message
    print package_entity

    # Update the details of a package.
    ckan.package_entity_get(package_name)
    package_entity = ckan.last_message
    package_entity['url'] = new_package_url
    ckan.package_entity_post(package_entity)


>>> myCkan = 

'''

__license__ = 'MIT'

import os, urllib2
import simplejson

class CkanClient(object):
    
    base_location = 'http://www.ckan.net/api/rest'
    resource_paths = {
        'Base': '/',
        'Package Register': '/package',
        'Package Entity': '/package',
        'Tag Register': '/tag',
        'Tag Entity': '/tag',
    }

    def __init__(self, base_location=None, api_key=None):
        if base_location is not None:
            self.base_location = base_location
        self.api_key = api_key

    def reset(self):
        self.last_status = None
        self.last_body = None
        self.last_headers = None
        self.last_message = None

    def open_url(self, location, data=None, headers={}):
        try:
            req = urllib2.Request(location, data, headers)
            self.url_response = urllib2.urlopen(req)
        except urllib2.HTTPError, inst:
            self.last_status = inst.fp.code
        else:
            self.last_status = self.url_response.code
            self.last_body = self.url_response.read()
            self.last_headers = self.url_response.headers
            try:
                self.last_message = self.loadstr(self.last_body)
            except ValueError:
                pass
    
    def get_location(self, resource_name, entity_id=None):
        base = self.base_location
        path = self.resource_paths[resource_name]
        if entity_id != None:
            path += '/' + entity_id
        return base + path

    def open_base_location(self):
        self.reset()
        url = self.get_location('Base')
        self.open_url(self.base_location)

    def package_register_get(self):
        self.reset()
        url = self.get_location('Package Register')
        self.open_url(url)
        return self.last_message

    def package_register_post(self, package_dict):
        self.reset()
        url = self.get_location('Package Register')
        data = self.dumpstr(package_dict)
        headers = {'Authorization': self.api_key}
        self.open_url(url, data, headers)

    def package_entity_get(self, package_name):
        self.reset()
        url = self.get_location('Package Entity', package_name)
        self.open_url(url)
        return self.last_message

    def package_entity_put(self, package_dict):
        self.reset()
        package_name = package_dict['name']
        url = self.get_location('Package Entity', package_name)
        data = self.dumpstr(package_dict)
        headers = {'Authorization': self.api_key}
        self.open_url(url, data, headers)

    def dumpstr(self, data):
        return simplejson.dumps(data)
    
    def loadstr(self, string):
        return simplejson.loads(string)
