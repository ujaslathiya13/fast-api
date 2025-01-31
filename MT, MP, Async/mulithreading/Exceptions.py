import threading
from threading import *
from time import sleep

def custom_hook(args):
    print("Excepiton occured in thread")
    print(args[0])
    print(args[1])
    print(args[2])
    print(args[3])

def display():
    for i in range(4):
        sleep(0.1)
        print("Hello:"+10)

def show():
    for i in range(4):
        print("Hello")
        sleep(0.5)

threading.excepthook = custom_hook

t1 = Thread(target=display)
t2 = Thread(target=show)

t1.start()
t2.start()
t1.join()
t2.join()

for i in range(4):
    print("BYE")