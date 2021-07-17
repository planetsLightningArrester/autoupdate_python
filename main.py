from threading import Timer,Thread,Event
from datetime import datetime
import sys

class newTimer(Thread):
    
    def __init__(self, event, timeOverflow):
        Thread.__init__(self)
        self.stopped = event
        self.timeOverflow = timeOverflow

    def run(self):
        while not self.stopped.wait(self.timeOverflow):
            print('ok')

if __name__ == "__main__":

    print('started')
    
    stopFlag = Event()
    timer = newTimer(stopFlag, 1)
    timer.start()

    # this will stop the timer
    # stopFlag.set()
