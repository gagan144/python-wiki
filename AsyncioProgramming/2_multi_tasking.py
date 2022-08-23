import os
import asyncio
import uuid
import time


async def mytask(name, limit=10):
    pid = os.getpid()
    print(f"[Mytask::{name}|PID={pid}] Start")
    for i in range(limit):
        print(f"[Mytask::{name}|PID={pid}]\tValue={i}")
        # Note: Do not use time.sleep() as will block the calls. Asyncio is
        # a non-blocking sleep mechanism
        await asyncio.sleep(0.1)

    print(f"[Mytask::{name}|PID={pid}] End.")
    return {
        "name": name,
        "message": "ok"
    }


async def main():
    N_TASKS = 20
    pid = os.getpid()
    print(f"[Main|PID={pid}] Start")

    start_time = time.time()

    # (1) Prepare list of tasks to be executed
    print(f"[Main|PID={pid}] Preparing {N_TASKS} tasks to be executed in parallel...")
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

    print(f"[Main|PID={pid}] End! Time taken: {time_taken_ms:.2f} ms")


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
[Main|PID=14728] Preparing 20 tasks to be executed in parallel...
[Main|PID=14728] Executing tasks asynchronously...
:
:
:
:
:
:
:
[Main|PID=14728] Results=[{'name': 'Iceandfire-1', 'message': 'ok'}, {'name': 'Iceandfire-2', 'message': 'ok'}, {'name': 'Iceandfire-3', 'message': 'ok'}, {'name': 'Iceandfire-4', 'message': 'ok'}, {'name': 'Iceandfire-5', 'message': 'ok'}, {'name': 'Iceandfire-6', 'message': 'ok'}, {'name': 'Iceandfire-7', 'message': 'ok'}, {'name': 'Iceandfire-8', 'message': 'ok'}, {'name': 'Iceandfire-9', 'message': 'ok'}, {'name': 'Iceandfire-10', 'message': 'ok'}, {'name': 'Iceandfire-11', 'message': 'ok'}, {'name': 'Iceandfire-12', 'message': 'ok'}, {'name': 'Iceandfire-13', 'message': 'ok'}, {'name': 'Iceandfire-14', 'message': 'ok'}, {'name': 'Iceandfire-15', 'message': 'ok'}, {'name': 'Iceandfire-16', 'message': 'ok'}, {'name': 'Iceandfire-17', 'message': 'ok'}, {'name': 'Iceandfire-18', 'message': 'ok'}, {'name': 'Iceandfire-19', 'message': 'ok'}, {'name': 'Iceandfire-20', 'message': 'ok'}]
[Main|PID=14728] End! Time taken: 1009.37 ms
[Python|PID=14728] End.
"""
