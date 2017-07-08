#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os,sys,atexit,time
limit = 60
class daemon:
    def __init__(self,task=None,pid_file=None):
        self.task = task
        self.pid_file = pid_file
    def _daemon(self):
        pid = os.fork()
        if pid: #父进程
            sys.exit(0)
        os.chdir('/')
        os.umask(0)
        os.setsid()
        pid = os.fork()
        if pid:
            sys.exit(0)
        sys.stderr.flush()
        sys.stdout.flush()
        with open('/dev/null') as read_null,open('/dev/null','w') as write_null:
            os.dup2(read_null.fileno(),sys.stdin.fileno())
            os.dup2(write_null.fileno(), sys.stdout.fileno())
            os.dup2(write_null.fileno(), sys.stderr.fileno())
        if self.pid_file:
            with open(self.pid_file,'w') as fn:
                fn.write(str(os.getpid()))
            atexit.register(os.remove(),self.pid_file)
        while(True):
            with open('./tmp/python.txt','aw') as fn:
                fn.write(str(time.time()))
            time.sleep(limit)
if __name__=='__main__':
    daemon(pid_file='./tmp/python.pid')