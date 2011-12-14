#!/usr/bin/env python

import subprocess
import threading
import sys

class Pinger():
    badHosts = []
    okHosts = []
    hostQueue = []
    lock = threading.Lock()
    ips = []
    threadsNum = 0

    def ping(self, host):
        print 'Pinging: ' + str(host)
        ret = subprocess.call('ping -c 1 -W 1 %s' % host,
                              shell=True,
                              stdout=open('/dev/null', 'w'),
                              stderr=subprocess.STDOUT)
        return ret == 0


    def popQueue(self):
        host = None

        self.lock.acquire()
        if len(self.hostQueue) > 0:
            host = self.hostQueue.pop()
        self.lock.release()

        return host


    def dequeue(self):
        while True:
            host = self.popQueue()
            if not host:
                return

            if self.ping(host):
                self.okHosts.append(host)
            else:
                self.badHosts.append(host)
                self.lock.acquire()
                self.lock.release()

            self.lock.acquire()
            self.lock.release()

    def start(self, ips, threads = 5):
        self.ips = ips
        self.threadsNum = threads

        threads = []

        for ip in self.ips:
            self.hostQueue.append(ip)

        for i in range(self.threadsNum):
            t = threading.Thread(target = self.dequeue)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

        return {'ok': self.okHosts, 'error': self.badHosts}
        #print 'err: ' + str(self.badHosts)
        #print 'ok: ' + str(self.okHosts)

if __name__ == '__main__':
    ips = [
        "ntp.rikshospitalet.no", "kutulu.rikshospitalet.no", "nonexisting", "10.161.1.1", "10.161.123.123",
        "ad", "rlx1024", "10.161.123.222", "10.161.111.111", "10.169.0.1", ".10.169.2.2", "kutulu",
        "lars-lx", "test", "unilab", "unilabtest", "10.199.22.1", "10.111.2.2", "10.111.3.3", "10.111.3.4",
        ]
    ping = Pinger()
    ping.start(ips, 10)
