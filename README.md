# Veeam Cloud Connect Tenants

The script works through the Veeam Backup Enterprise Manager RESTful API and serves to display information about Tenants. Displays the name of tenant, size of backup, number of VM in backup, number of VM in replica and computer resources for replica.

Example:
```
./veeam_stats_cc.py -tenants
Tenant name: KorP_agent
Used space: 0.0 (Quota: 10) Gb
Backuped VM: 0
Replicated VM: 0
----------------------------------------
Tenant name: KorP
Used space: 160.48 (Quota: 200) Gb
Backuped VM: 12
Replicated VM: 1
Compute resources for replica:
	CPU count: 1
	Memory usage: 4096 Mb
	Used space: 12.0 Gb
----------------------------------------
```

As a setting, you must specify variables
```
self.address = 'https://IP:9398/api/'
self.username = 'username'
self.password = 'password'
```
