#!/usr/bin/env python

import json
import subprocess as su


class AwsGetServers:
    """
    aws command wrapper 
    """
    _servers={}
    _regions=[]
    _fetch_regions=True
    _accepted_tags=[]
 
    def  __init__(self, accepted_tags=[], regions=[]):
        """
        Set regions, tags
        """
        self._regions=regions
        self._accepted_tags=accepted_tags
        
        if regions:
            self._fetch_regions=False
 
    def _get_regions(self):
        """
        Get all available regions
        """
        regions_json = su.Popen("aws ec2 describe-regions", stdout=su.PIPE, stderr=su.PIPE,  shell=True).stdout.read()
        regions_object = json.loads(regions_json)
        self._process_regions(regions_object)
        
    def _process_regions(self,regions_object):
        """
        Save all available regions
        """
        for region in regions_object['Regions']:
            self._regions.append(region['RegionName'])

    def _get_servers(self, region=""):
        """
        Exec aws cmd for region(s)
        """
        for_region=""
        if region:
            for_region="AWS_DEFAULT_REGION=\"%s\" " % region

        servers_json = su.Popen("%s aws ec2 describe-instances" % for_region, stdout=su.PIPE, stderr=su.PIPE,  shell=True).stdout.read()
        if servers_json[0:1] == "{":
            servers_object = json.loads(servers_json)
            self._process_servers(servers_object) 
        
    def _process_servers(self, servers_object):
        """
        Process json servers 
        """
        servers = self._servers
        for rese in servers_object['Reservations']:
            for inst in rese['Instances']:
                if inst['State']['Name'] == 'running':
                    for tag in inst['Tags']:              
                        if len(self._accepted_tags)==0 or tag['Key'] in self._accepted_tags:
                            cc = inst['Placement']['AvailabilityZone'][0:2]
                            k = tag['Value']+" "+inst['InstanceType']+" "+cc
                            if servers.get(k) is None:
                                servers[k] = []
                            servers[k].append( inst['PublicIpAddress'] )

        servers.keys().sort()
        self._servers = servers

    def get_servers(self):
        """
        Get regions get servers for all specified regions 
        """
        if self._fetch_regions :
            self._get_regions()
 
        print "Using regions: "
        print self._regions
        
        if self._regions:
            for region in self._regions:
                self._get_servers(region)
        else:
            self._get_servers()

        return self._servers

if __name__ == "__main__":
    print AwsGetServers(accepted_tags=[], regions=[]).get_servers()
 

