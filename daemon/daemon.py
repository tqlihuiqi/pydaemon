# -*- coding:utf-8 -*-

import os
import signal
import sys
import time

import psutil
import setproctitle


class Daemon(object):

    def __init__(self, pidfile, target=None, args=(), procname=None):
        """ Initialization configuration

        :param pidfile: pid file
        :type pidfile: str
        :param target: application function
        :type target: str
        :param args: parameters of application function
        :type args: tuple / list
        :param procname: process name, if no name is specified, will default to function name
        :type procname: str
        """

        self.target = target
        self.args = args
        self.procname = procname
        self.pidfile = pidfile


    def output(self, message):
        """ Write message to STDOUT

        :param message: to output message
        :type message: str
        """

        sys.stdout.write("%s\r\n" % message)
        sys.stdout.flush()


    def __get_pid(self):
        """ Query the daemon process id

        :return: pid / None
        """

        if os.path.exists(self.pidfile):
            pid = open(self.pidfile, "r").readline()
            
            if pid and int(pid) in psutil.pids():
                return int(pid)
    
        return None


    def __fork(self):
        """ Fork the daemon process """
        
        for i in range(2):
            try:
                pid = os.fork()

                if pid > 0:
                    sys.exit(0)
            except OSError:
                self.output("fork daemon process failed.")
                sys.exit(1)

            if i == 1:
                os.chdir("/")
                os.setsid()
                os.umask(0o22)

        open(self.pidfile, "w+").write("%s" % os.getpid())
        setproctitle.setproctitle(self.procname or self.target.__name__)


    def daemon(self, target):
        """ The daemon decorator """

        self.target = target
        
        def _decor(*args, **kwargs):
            self.__fork()
            target(*args, **kwargs)
        
        return _decor


    def start(self):
        """ Start the daemon process """

        if not self.target:
            self.output("target is not specified")
            sys.exit(2)

        self.output("Starting")

        self.__fork()
        self.target(*self.args)


    def stop(self):
        """ Stop the daemon process """

        pid = self.__get_pid()
        retries = 5

        while pid:
            if retries > 0:
                sig = signal.SIGTERM
            else:
                sig = signal.SIGKILL

            os.kill(pid, sig)

            retries -= 1
            time.sleep(0.1)
            pid = self.__get_pid()
    
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)
    
        self.output("Stopped")


    def restart(self):
        """ Restart the daemon process """

        self.stop()
        self.start()


    def status(self):
        """ Check the daemon process status """

        pid = self.__get_pid()
    
        if pid:
            self.output("Alive, PID: %s" % pid)
        else:
            self.output("Stopped")

