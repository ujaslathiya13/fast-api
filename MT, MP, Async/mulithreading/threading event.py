import time
from threading import Thread, Event


def writing_file(event):
    with open("Files/ThreadLog.txt","a") as file:
        for i in range(10):
            time.sleep(0.100)
            print(f'Printed line {i}')
            file.write(f"line {i} : Python {time.time()}")

    event.set()

def count_words(event):

    print("waiting")
    event.wait()
    print(("writing complete, started counting"))
    word_count = 0

    with open("Files/ThreadLog.txt", "r") as file:
        for line in file:
            words = line.split()
            word_count += len(words)

    print(f"no of words in file : {word_count}")

event = Event()

t1 = Thread(target=writing_file, args=(event,))
t2 = Thread(target=count_words, args=(event,))

t1.start()
t2.start()

t1.join()
t2.join()
