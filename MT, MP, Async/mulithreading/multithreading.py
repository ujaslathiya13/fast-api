import time
from threading import Thread

class Print_Details:

    @classmethod
    def writeNumbers(self, n: int):
        for i in range(n):
            print(f"thread 1 : {i}\n")
            time.sleep(0.2)

    @staticmethod
    def writeLatters():
        for letter in 'abcdefghij':
            print(f"thread 2 : {letter}\n")
            time.sleep(0.2)

    def write_Hello(self, n: int):
        for i in range(n):
            print(f"thread 3 : Hello\n")
            time.sleep(0.2)

stat_time = time.time()

# Create object to give target for methods defined class
obj = Print_Details()


t1 = Thread(target=Print_Details.writeNumbers, args=(10,))  # Give Reference of class name of class-methods and instance-methods
t2 = Thread(target=Print_Details.writeLatters)
t3 = Thread(target=obj.write_Hello, args=(10,))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

end_time = time.time()