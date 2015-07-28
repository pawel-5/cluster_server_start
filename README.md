
Start cssh (cluster ssh with few clicks).

Project contains:
  ServerGui.py      - gui wrapper for servers
  AwsGetServers.py  - fetch running servers using aws command (http://aws.amazon.com/cli/) need to have this to fetch running IPs
  cluster_server_start.py - start file with defaults settings (modify to your own needs)  

It should be simple to add new server providers (AwsGetServers.py) to extend for other cloud computing services.



