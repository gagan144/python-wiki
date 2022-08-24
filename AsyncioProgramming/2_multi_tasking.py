"""
Python script to perform multitasking asynchronously.
"""
import os
import asyncio
import time


async def mytask(name, limit=10):
    pid = os.getpid()

    print(f"[Mytask::{name}|PID={pid}] Start")
    start_time = time.time()

    for i in range(limit):
        print(f"[Mytask::{name}|PID={pid}]\tValue={i}")
        # Note: Do not use time.sleep() as will block the calls. Asyncio is
        # a non-blocking sleep mechanism
        await asyncio.sleep(0.1)

    time_taken_ms = (time.time() - start_time) * 1000
    print(f"[Mytask::{name}|PID={pid}] End.")

    return {
        "name": name,
        "message": "ok",
        "time_taken_ms": round(time_taken_ms, 2)
    }


async def main():
    N_TASKS = 1000
    pid = os.getpid()
    print(f"[Main|PID={pid}] Start")

    start_time = time.time()

    # (1) Prepare list of tasks to be executed
    print(f"[Main|PID={pid}] Preparing {N_TASKS} tasks to be executed asynchronously...")
    list_tasks = []
    for i in range(N_TASKS):
        list_tasks.append(
            mytask(name=f"Iceandfire-{(i+1)}", limit=10)
        )

    # (2) Execute all tasks asynchronously
    print(f"[Main|PID={pid}] Executing tasks asynchronously...")
    results = await asyncio.gather(*list_tasks, return_exceptions=True)
    print(f"[Main|PID={pid}] Results={results}")

    time_taken_ms = (time.time()-start_time)*1000

    print(f"[Main|PID={pid}] End! Time taken: {time_taken_ms:.2f} ms to run {N_TASKS} tasks.")


if __name__ == '__main__':
    pid = os.getpid()
    print(f"[Python|PID={pid}] Start")
    asyncio.run(main())
    print(f"[Python|PID={pid}] End.")


"""
OUTPUT
-----------

[Python|PID=14728] Start
[Main|PID=14728] Start
[Main|PID=14728] Preparing 100000 tasks to be executed in parallel...
[Main|PID=14728] Executing tasks asynchronously...
:
:
:
:
:
:
:
 ... {'name': 'Iceandfire-99999', 'message': 'ok', 'time_taken_ms': 17395.25}, {'name': 'Iceandfire-100000', 'message': 'ok', 'time_taken_ms': 17395.24}]
[Main|PID=15447] End! Time taken: 20345.96 ms to run 100000 tasks.
[Python|PID=15447] End.
"""
