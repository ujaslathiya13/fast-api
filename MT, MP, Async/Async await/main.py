import asyncio
import time
from fastapi import FastAPI

app = FastAPI()

"""
Runs in main Thread
no awaitable operation, function execution paused, blocking I/O
request handles sequentially
"""
@app.get('/async-def') #processed sequentially
async def endpoint1():
    print("Hello")
    time.sleep(5)
    print("Bye")

"""
Runs in main Thread
non-blocking I/O,
awaited
function execution paused
"""
@app.get('/async-await') #processed concurrently
async def endpoint2():
    print("Hello")
    await asyncio.sleep(5)
    print("Bye")

"""
Runs in Separate Threads
"""
@app.get('/def') # processed parallely
def endpoint3():
    print("Hello")
    time.sleep(5)
    print("Bye")



