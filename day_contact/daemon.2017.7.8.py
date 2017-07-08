#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os,sys,atexit,time
limit = 60
class daemon:
    def __init__(self,task=None,pid_file=None):
        self.task = task
        self.pid_file = pid_file
    def _daemon(self):
        try:
            pid = os.fork()
            if pid: #父进程
                sys.exit(0)
            os.chdir('/')
            os.umask(222)
            os.setsid()
            pid = os.fork()
            if pid:
                sys.exit(0)
            print(os.getpid())
            sys.stderr.flush()
            sys.stdout.flush()
            with open('/dev/null') as read_null,open('/dev/null','w') as write_null:
                os.dup2(read_null.fileno(),sys.stdin.fileno())
                os.dup2(write_null.fileno(), sys.stdout.fileno())
                os.dup2(write_null.fileno(), sys.stderr.fileno())
            if self.pid_file:
                with open(self.pid_file,'w') as fn:
                    fn.write(str(os.getpid()))
                atexit.register(os.remove,self.pid_file)
            while(True):
                with open('./tmp/python.txt','a+') as fn:
                    fn.write(str(time.time())+"\n")
                time.sleep(limit)
        except Exception as e:
            pass
        finally:
            os.remove(self.pid_file)
if __name__=='__main__':
    mydaemon = daemon(pid_file='./tmp/python.pid')
    mydaemon._daemon()
