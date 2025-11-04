import multiprocessing
import time 
import threading

def printProcessInfo(sleep=None):
    if sleep != None:
        time.sleep(sleep)
    print("==== Process Info ====")
    print("current.process => ", multiprocessing.current_process().name)
    print("current.process.id => ", multiprocessing.current_process().pid)
    print("current.thread => ",threading.current_thread().name)
    print("======================")

def testFunc():
    printProcessInfo()
    return 456

def launchProcess():
    p = multiprocessing.Process(target=testFunc)
    p.start()
    p.join()#will wait 


