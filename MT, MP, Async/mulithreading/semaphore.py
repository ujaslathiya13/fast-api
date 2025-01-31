import threading
from time import sleep


def read_file(i : int,filename):
    with semaphore:
        with open(f"Files/{filename}",'r') as file:
            data = file.read()
            for j in range(5):
                print(f"Thread {i} : {data}")
                sleep(0.5)


semaphore = threading.Semaphore(2)

threads = []

for i in range(1,6):
    thread = threading.Thread(target=read_file, args=(i, f"file{i}.txt"))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()