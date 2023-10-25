A utility to sync docker images between 2 machines while transferring only the changed layers

# Installation
`pipx install docker-remote-sync` or `pipinstall docker-remote-sync`

# Usage
```
usage: docker-remote-sync [-h] [--port PORT] image_name remote destination_folder

Utility to sync updated docker layers between 2 machines

positional arguments:
  image_name          Docker image (along with tag) on local machine
  remote              Address of remote with
  destination_folder  Cache folder on destination

options:
  -h, --help          show this help message and exit
  --port PORT         Alternate ssh port on remote

Do not delete the cache folder on remote machine to take advantage of incremental file sync
The tar file on remote which is the snapshot of local docker image with be at location <<destination_folder>>.tar
This folder can be "loaded" into docker using `docker load -i <<destination_folder>>.tar`
```
Example:
```
docker-remote-sync myalpine:latest remotehost /tmp/myalpine_syncfolder
```