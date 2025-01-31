from threading import *
from time import sleep

l = RLock()

def print1():
    l.acquire()
    print(("Printing First Line..."))
    sleep(2)
    l.release()

def print2():
    l.acquire()
    print("Printing Second Line... ")
    sleep(2)
    l.release()

def main():
    l.acquire()
    print1() #function 1
    print2() # function 2
    l.release()

t1= Thread(target=main())
t1.start()
t1.join()
print("Programme completed")
