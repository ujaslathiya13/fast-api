import threading

lock = threading.Lock()

def write_file(i : int):
    with lock:
        with open(f"Files/ThreadLog2.txt",'a') as file:
            file.write(f"Theread {i} : Python")

threads = []

for i in range(1,16):
    thread = threading.Thread(target=write_file, args=(i,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("File updated")