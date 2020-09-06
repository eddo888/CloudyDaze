# CloudyDaze

bunch of usefull scripts for managing your cloud

## mySG.py

Tool to add your current IP address to the security group permissions.

Please add the following patameter to your ~/.aws/config file
```
mysg=sg_...
```

### help
```
$ ./mySG.py --help
usage: mySG.py [-h] [-p PROFILE] [-u URL] [-v] {enable,granted,myip,replace,revoke,args} ...

positional arguments:
  {enable,granted,myip,replace,revoke,args}
                        operations
    enable
    granted
    myip
    replace
    revoke
    args                print the values for the args

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        default=default
  -u URL, --url URL     default=https://api.ipify.org?format=json
  -v, --verbose         verbose logging
```

## myEC2.py

simple tool to start or stop ec2 instances

### help
```
$ ./myEC2.py --help
usage: myEC2.py [-h] [-p PROFILE] [-v] {list,start,stop,args} ...

positional arguments:
  {list,start,stop,args}
                        operations
    list
    start
    stop
    args                print the values for the args

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        default=default
  -v, --verbose         verbose logging
```
