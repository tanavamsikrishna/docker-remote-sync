A utility to sync docker images between two machines while transferring only the changed layers

# Setup
### Requirements
Apart from `docker`, `rsync` is needed on both the machines.

### Installation
`pipx install docker-remote-sync` or `pip install docker-remote-sync`


# Usage
```
usage: docker-remote-sync [-h] [--port PORT] [--docker-cmd DOCKER_CMD] image_name remote remote_cache_folder

Utility to sync updated docker layers between two docker host machines

positional arguments:
  image_name            Docker image on local machine
  remote                Address of remote
  remote_cache_folder   Cache folder on remote

options:
  -h, --help            show this help message and exit
  --port PORT           Alternate ssh port on remote
  --docker-cmd DOCKER_CMD
                        Alternate docker command. Defaults to `docker`. Eg. `colima x - docker` or `podman`

○ Do not delete the cache folder on the remote machine to be able to take advantage of incremental file sync
○ Example usage: `docker-remote-sync alpine:latest remotehost "~/my_alpine_cache"````

- Do not delete the cache folder on the remote machine to be able to take advantage of incremental file sync

Example:
`docker-remote-sync myalpine:latest remotehost "~/myalpine_cache"`
