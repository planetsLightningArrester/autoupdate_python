import sys
import time
import subprocess
import os
from threading import Timer,Thread,Event
import platform

mainProcess = 0
targetFolder = '/home/pi/'

class newTimer(Thread):
    
    def __init__(self, event, timeOverflow):
        Thread.__init__(self)
        self.stopped = event
        self.timeOverflow = timeOverflow

    def run(self):
        while not self.stopped.wait(self.timeOverflow):
            print('ok')

def internetAvailable():
    if platform.system() == 'Linux':
        pingProcess = subprocess.Popen('ping -c 1 www.google.com', stdout=open(os.getcwd() + '/log/ping.log', 'wb'))
    else:
        pingProcess = subprocess.Popen('ping -n 1 www.google.com', stdout=open(os.getcwd() + '/log/ping.log', 'wb'))
    pingProcess.wait()

    if (pingProcess.returncode == 0):
        pingProcess.terminate()
        return True
    else:
        pingProcess.terminate()
        return False

def checkForUpdates():
    global mainProcess

    if internetAvailable():
        print('Internet available.')
        if updateAvailable():
            print('Update available.')
            
            update()

            if mainProcess:
                mainProcess.terminate()

            mainProcess = subprocess.Popen('python main.py')
            # mainProcess = subprocess.Popen('python main.py', stdout=open(os.getcwd() + '/log/main.log', 'wb'))
    try:
        time.sleep(10)
        checkForUpdates()
    except KeyboardInterrupt:
        mainProcess.terminate()
        sys.exit()
        

def updateAvailable():
    if platform.system() == 'Linux':
        differenceBetweenRemoteAndLocal = os.popen('sudo git -C ' + targetFolder + ' diff').read()
    else:
        differenceBetweenRemoteAndLocal = os.popen('git diff').read()

    if differenceBetweenRemoteAndLocal:
        return True
    else:
        return False


def update():
    if platform.system() == 'Linux':
        updateResult = os.popen('sudo git -C ' + targetFolder + ' reset --hard HEAD;sudo git -C ' + targetFolder + ' checkout master; sudo git -C ' + targetFolder + ' pull -f origin master').read()
    else:
        subprocess.Popen('git reset --hard HEAD').wait()
        subprocess.Popen('git checkout master').wait()
        subprocess.Popen('git pull origin master').wait()

    print('Code updated.')

    # if(updateResult.find("Updating...") != -1):
    #     print("Code updated.")
    # else:
    #     print("Couldn't update.")

if __name__ == "__main__":
    try:
        Thread(target=checkForUpdates).start()

    except KeyboardInterrupt as event:
        if mainProcess:
            mainProcess.terminate()
        sys.exit()
