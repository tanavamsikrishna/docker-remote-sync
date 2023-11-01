A utility to sync docker images between two machines while transferring only the changed layers

# Setup
### Requirements
Apart from `docker`, `rsync` is needed on both the machines.

### Installation
`pipx install docker-remote-sync` or `pip install docker-remote-sync`


# Usage
```
usage: docker-remote-sync [-h] [--port PORT] image_name remote remote_cache_folder

Utility to sync updated docker layers between two docker host machines

positional arguments:
  image_name           Docker image (along with tag) on local machine
  remote               Address of remote with
  remote_cache_folder  Cache folder on remote

options:
  -h, --help           show this help message and exit
  --port PORT          Alternate ssh port on remote
```

- Do not delete the cache folder on the remote machine to be able to take advantage of incremental file sync

Example:
`docker-remote-sync myalpine:latest remotehost "~/myalpine_cache"`
