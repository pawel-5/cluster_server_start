#!/usr/bin/env python

import AwsGetServers
import ServersGui

# list of tags (values) to filter
accepted_tags=[]

# list of regions to fetch servers from if not set 
# will fetch for all available regions
regions=[]

# ips python map where key is "tag" name  and value array of IPs
ips = AwsGetServers.AwsGetServers(accepted_tags, regions).get_servers()

# extra params for gui in form of python map 
# key is regex match for tag with touple of 
# user and ssh key to use for it
# example {'webservers': ('apache', 'apache.key')} 
cssh_params = {}
ServersGui.ServersGui(ips, cssh_params)

