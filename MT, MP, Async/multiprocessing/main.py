import multiprocessing
import requests
import concurrent.futures

def download_file(link: str, filename: str):
    response = requests.get(link)
    open(f"images/{filename}.jpg",'wb').write(response.content)
    print(f"finished downloading {filename}.jpg")
    return f"{filename}.jpg"

# Lorem Picsum URL ( Random Images )
url = "https://picsum.photos/200/300"

# By Using Multiprocessing module
pros = []
for i in range(1,11):
    p = multiprocessing.Process(target=download_file, args=[url,i])
    p.start()
    pros.append(p)

for p in pros:
    p.join()

# By Using Process Pool Executor
with concurrent.futures.ProcessPoolExecutor() as executor:
    url_list = [url for i in range(10)]
    filename_list = [i for i in range(11,21)]
    results = executor.map(download_file, url_list, filename_list)
    for r in results:
        print(r)
