
Python daemon process
====================

Daemonize your Python program so it can continue running in the background.


Usage
---------------------

### General method

``` python
import time
from daemon import Daemon

def program(total):
    count = 0
    while count <= total:
        time.sleep(1)
        count += 1

proc = Daemon(target=program, args=(100,), procname="myDaemonProgram", pidfile="/tmp/program.pid")
proc.start()
```
```shell
localhost: lihuiqi$ ps -ef |grep myDaemonProgram
  501 98023     1   0  1:35下午 ??         0:00.00 myDaemonProgram 
```

### Decorator method

``` python
import time
from daemon import Daemon

proc = Daemon(procname="myDaemonProgram", pidfile="/tmp/program.pid")

@proc.daemon
def program(total):
    count = 0
    while count <= total:
        time.sleep(1)
        count += 1


program(total=100)
```
```shell
localhost: lihuiqi$ ps -ef |grep myDaemonProgram
  501 98031     1   0  1:49下午 ??         0:00.00 myDaemonProgram 
```


Actions
---------------------

* `start()` - starts the daemon (creates PID and daemonizes).
* `stop()` - stops the daemon (stops the child process and removes the PID).
* `restart()` - does `stop()` then `start()`.
* `status()` - checks the daemon status.

