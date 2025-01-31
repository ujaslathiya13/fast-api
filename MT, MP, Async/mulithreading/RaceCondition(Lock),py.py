from threading import *
from time import sleep

lock = Lock()

class Bus:
    def __init__(self,name,available_seats,l):
        self.name = name
        self.available_seats = available_seats
        self.l = l

    def reserve(self,need_seats):
        self.l.acquire()
        print("Available seats are : ",self.available_seats)
        if self.available_seats >= need_seats:
            nm = current_thread().name
            # update no of ticket in database
            print(f"{need_seats} are allocated to {nm}")
            self.available_seats -= need_seats
        else:
            print("Sorry!seats are not available")
        self.l.release()

b1=Bus("BM Travels",2,lock)
t1 = Thread(target=b1.reserve,args=(1,),name="Yash")
t2 = Thread(target=b1.reserve,args=(1,),name="Raj")
t3 = Thread(target=b1.reserve,args=(1,),name="Ujas")
t1.start()
t2.start()
t3.start()
