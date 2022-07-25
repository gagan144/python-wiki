# Python script as a service through Linux Systemctl

**Last Updated On**: 25-Jul-2022

**References:**
  - [Best] https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267
  - [Some cool options] https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6

## Steps
Following are the steps to register a python script as a linux service through systemctl:

- Create a service file in `/etc/systemd/system/`. For instance, `/etc/systemd/system/myservice.service`:
  ```
  [Unit]
  Description=This is service for my custom python script
  After=network.target
  StartLimitBurst=5
  StartLimitIntervalSec=10
  
  [Service]
  User=ubuntu
  Type=simple
  WorkingDirectory=/home/ubuntu/projects/python-wiki/PythonScriptAsLinuxService/example
  ExecStart=/bin/bash -c 'cd /home/ubuntu/projects/python-wiki/PythonScriptAsLinuxService/example/ && source /home/ubuntu/PythonEnv/venv/bin/activate && python myservice.py'
  Restart=always
  
  [Install]
  WantedBy=multi-user.target 
  ```

- Reload the systemctl daemon:
  ```shell
  sudo systemctl daemon-reload
  ```
  
- Let’s enable our service so that it doesn't get disabled if the server restarts:
  ```shell
  sudo systemctl enable myservice.service
  ```

- Start your service:
  ```shell
  sudo systemctl start myservice.service
  ```

## Management
Following is the syntax to manage your service:
```shell
sudo systemctl start|stop|restart|status myservice.service
```
OR
```shell
sudo systemctl start|stop|restart|status myservice
```
