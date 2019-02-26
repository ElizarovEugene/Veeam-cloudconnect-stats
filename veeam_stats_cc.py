#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import collections
import re
import requests
import sys
import urllib3

class Veeam:
    #Initialize variable and get API authorize token
    def __init__(self):
        urllib3.disable_warnings()
        self.address = 'https://IP:9398/api/'
        self.username = 'LOGIN'
        self.password = 'PASSWORD'
        
        self.session_id = self.get_authorize_token()
        self.headers = {'X-RestSvcSessionId': self.session_id['session_id'], 'Content-Type': 'application/xml'}

    #Get API authorize token
    def get_authorize_token(self):
        try:
            r = requests.post(self.address + 'sessionMngr/?v=latest', auth=(self.username, self.password), verify=False)
            if r.status_code != 201:
                raise Exception('Authorization faileds')
            return {'session_id': r.headers['X-RestSvcSessionId']}
        except Exception:
            sys.exit('Authorization faileds')
            
    #Get tenant compute resources
    def get_compute_resources(self, id):
        r = requests.get(self.address + '/cloud/tenants/' + id + '/computeResources', headers=self.headers, verify=False)
        soup = BeautifulSoup(r.text, 'xml')
        
        MemoryUsageMb = soup.find('MemoryUsageMb').getText()
        CPUCount = soup.find('CPUCount').getText()
        StorageUsageGb = soup.find('StorageUsageGb').getText()
        
        print 'Compute resources for replica:'
        print '\tCPU count: ' + str(CPUCount)
        print '\tMemory usage: ' + str(MemoryUsageMb) + ' Mb'
        print '\tUsed space: ' + str(float(StorageUsageGb)) + ' Gb'
            
    #Get tenants info
    def get_tenants_info(self, id):
        r = requests.get(self.address + 'cloud/tenants/' + id + '?format=Entity', headers=self.headers, verify=False)
        soup = BeautifulSoup(r.text, 'xml')
        
        UsedQuota = soup.find('UsedQuota').getText()
        Quota = soup.find('Quota').getText()
        BackupCount = soup.find('BackupCount').getText()
        ReplicaCount = soup.find('ReplicaCount').getText()
        
        print 'Used space: ' + str(round(float(UsedQuota) / 1024, 2)) + ' (Quota: ' + str(int(Quota) / 1024) + ') Gb'
        print 'Backuped VM: ' + str(BackupCount)
        print 'Replicated VM: ' + str(ReplicaCount)
        if int(ReplicaCount) > 0:
            self.get_compute_resources(id)
        print '-' * 40
            
    #Get tenants
    def get_tenants(self):
        r = requests.get(self.address + 'cloud/tenants', headers=self.headers, verify=False)
        soup = BeautifulSoup(r.text, 'xml')
        tenants = soup.findAll('Ref')
        for tenant in tenants:
            name = tenant.get('Name')
            id = tenant.get('UID').replace('urn:veeam:CloudTenant:', '')
            print 'Tenant name: ' + name
            self.get_tenants_info(id)
    

if __name__ == "__main__":
    veeam = Veeam()
    if len(sys.argv) == 1:
        print 'Используйте ключи: -tenants'
        sys.exit(0)
    if sys.argv[1] == '-tenants':
        veeam.get_tenants()
