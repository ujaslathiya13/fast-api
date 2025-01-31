import threading
import time
from time import sleep

e = threading.Event()

def switch_light():
    while True:
        print("Light is Green")
        e.set()
        sleep(5)
        print("Light is Red")
        e.clear()
        sleep(5)

def traffic_message():
    e.wait()
    while e.is_set():
        print("You can go!")
        sleep(1)
        e.wait()

t1 = threading.Thread(target=switch_light)
t2 = threading.Thread(target=traffic_message)
t1.start()
t2.start()
