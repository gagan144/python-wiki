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
    pid = os.getpid()
    print(f"[Main|PID={pid}] Start")

    start_time = time.time()

    # # --- Method-1 ---
    # # Prepare a coroutine; THis does not execute the task
    # task1 = mytask(name=str(uuid.uuid4()), limit=10)
    # print(f"[Main|PID={pid}] task1={task1}")
    #
    # # Execute function synchronously using 'await' syntax
    # await task1
    # # --- /Method-1 ---

    # --- Method-2 ---
    # Creating asyncio task to receive a future. This will execute the task asynchronously as soon as
    # the program control encounters an await statement (for this task or for something else) or parent function end
    task1 = asyncio.create_task(mytask(name=str(uuid.uuid4()), limit=10))
    print(f"[Main|PID={pid}] task1={task1}, state={task1._state}")

    # Use 'await' if you want to wait for the task to finish synchronously and get result.
    # You can also use `task1.result()` to obtain the result only if the task is finished.
    result = await task1
    print(f"[Main|PID={pid}] Task State='{task1._state}', Result={result}")
    # --- /Method-2 ---

    print(f"[Main|PID={pid}] Sleeping for a while...")
    await asyncio.sleep(5)
    print(f"[Main|PID={pid}] Sleep time over.")

    time_taken_ms = (time.time()-start_time)*1000

    print(f"[Main|PID={pid}] End! Time taken: {time_taken_ms:.2f} ms")


if __name__ == '__main__':
    pid = os.getpid()
    print(f"[Python|PID={pid}] Start")
    asyncio.run(main())
    print(f"[Python|PID={pid}] End.")


"""
OUTPUT
---------------
[Python|PID=14655] Start
[Main|PID=14655] Start
[Main|PID=14655] task1=<Task pending name='Task-2' coro=<mytask() running at ..../1_basic_asyncio.py:7>>, state=PENDING
[Mytask::83faf44f-39e1-4d8c-a83b-36d943f84c47|PID=14655] Start
[Mytask::83faf44f-39e1-4d8c-a83b-36d943f84c47|PID=14655]	Value=0
[Mytask::83faf44f-39e1-4d8c-a83b-36d943f84c47|PID=14655]	Value=1
[Mytask::83faf44f-39e1-4d8c-a83b-36d943f84c47|PID=14655]	Value=2
[Mytask::83faf44f-39e1-4d8c-a83b-36d943f84c47|PID=14655]	Value=3
[Mytask::83faf44f-39e1-4d8c-a83b-36d943f84c47|PID=14655]	Value=4
[Mytask::83faf44f-39e1-4d8c-a83b-36d943f84c47|PID=14655]	Value=5
[Mytask::83faf44f-39e1-4d8c-a83b-36d943f84c47|PID=14655]	Value=6
[Mytask::83faf44f-39e1-4d8c-a83b-36d943f84c47|PID=14655]	Value=7
[Mytask::83faf44f-39e1-4d8c-a83b-36d943f84c47|PID=14655]	Value=8
[Mytask::83faf44f-39e1-4d8c-a83b-36d943f84c47|PID=14655]	Value=9
[Mytask::83faf44f-39e1-4d8c-a83b-36d943f84c47|PID=14655] End.
[Main|PID=14655] Task State='FINISHED', Result={'name': '83faf44f-39e1-4d8c-a83b-36d943f84c47', 'message': 'ok'}
[Main|PID=14655] Sleeping for a while...
[Main|PID=14655] Sleep time over.
[Main|PID=14655] End! Time taken: 6009.29 ms
[Python|PID=14655] End.

Process finished with exit code 0
"""
