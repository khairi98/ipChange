import socket
import socks
import requests
import sys
import os
import time
import psutil
import apt #sudo apt-get install python-apt

def connectToTor():
    print('Setting proxy...')
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
    socket.socket = socks.socksocket
    print("IP Changed")

def checkIfTorIsRunning():
    torRunning = False
    for process in psutil.process_iter(attrs = ['name']):
        if(process.info['name'] == 'tor'):
            torRunning = True
    return torRunning

def checkIfTorIsInstalled():
    torInstalled = False
    cache = apt.cache.Cache()
    if cache['tor'].is_installed:
            torInstalled = True
    return torInstalled

def runTorService():
     print('Enabling Tor Service...')
     os.system('sudo service tor start') #Start tor service
     time.sleep(5)

def changeIP():
    socks.setdefaultproxy()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 9050))
    s.send('AUTHENTICATE\r\n')
    response = s.recv(128)
    if response.startswith('250'):
        s.send('SIGNAL NEWNYM\r\n')
    s.close()
    connectToTor()

def testIP():
    response = requests.get('http://ipecho.net/plain').text
    print(response)
    
def main():
    if checkIfTorIsInstalled() == False:
        sys.exit('Please Install Tor...')
    if checkIfTorIsRunning() == False:
        runTorService()
    connectToTor()
    testIP()
    time.sleep(5)
    changeIP()
    testIP()


if __name__ == '__main__':
    main()