A utility to sync docker images between 2 machines while transferring only the changed layers

# Installation
`pipx install docker-remote-sync` or `pip install docker-remote-sync`

# Usage
```
usage: docker-remote-sync [-h] [--port PORT] image_name remote destination_folder

Utility to sync updated docker layers between 2 docker host machines

positional arguments:
  image_name          Docker image (along with tag) on local machine
  remote              Address of remote with
  destination_folder  Cache folder on destination

options:
  -h, --help          show this help message and exit
  --port PORT         Alternate ssh port on remote

○ Do not delete the cache folder on the remote machine to be able to take advantage of incremental file sync
○ The tar file on the remote, which is the snapshot of the local Docker image, will be at location <<destination_folder>>.tar
○ This tar file can be "loaded" into Docker using `docker load -i <<destination_folder>>.tar`
○ Example usage: `docker-remote-sync myalpine:latest remotehost /tmp/myalpine_remotefolder`
```

Example:
```
docker-remote-sync myalpine:latest remotehost /tmp/myalpine_syncfolder
```