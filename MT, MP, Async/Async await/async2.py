import asyncio

async  def main():
    task = asyncio.create_task(second_task())
    print("Start A")
    await asyncio.sleep(1)
    print("End A")
    await task

async def second_task():
    print("Start B")
    await asyncio.sleep(2)
    print("End B")

asyncio.run(main())