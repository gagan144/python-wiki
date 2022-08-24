"""
Python script to call REST API asynchronously.
"""
import time
import asyncio
import aiohttp  # pip install aiohttp
# import requests   # WARNING! Do not use requests module as it is synchronous


# Ref: https://mixedanalytics.com/blog/list-actually-free-open-no-auth-needed-apis/
API_URL = "https://dog.ceo/api/breeds/image/random"


async def fetch_http_data(name, session: aiohttp.ClientSession) -> dict:
    """
    Task to fetch data from an REST API.
    """

    print(f"[HttpFetch::{name}] Start - Getting data from '{API_URL}'...")
    start_time = time.time()

    response = await session.get(API_URL)
    response_data = await response.json()

    time_taken_ms = (time.time() - start_time) * 1000
    print(f"[HttpFetch::{name}] End.")

    return {
        "name": name,
        "response": {
            "url": response.url.path,
            "status": response.status,
            "data": response_data
        },
        "time_taken_ms": round(time_taken_ms, 2)
    }


async def main():
    N_TASKS = 50
    print(f"[Main] Start")

    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        # (1) Prepare list of tasks to be executed
        print(f"[Main] Preparing {N_TASKS} tasks to be executed asynchronously...")
        list_tasks = []
        for i in range(N_TASKS):
            list_tasks.append(
                fetch_http_data(name=f"Task-{(i+1)}", session=session)
            )

        # (2) Execute all tasks asynchronously
        # This should be placed inside session scope
        print(f"[Main] Executing tasks asynchronously...")
        results = await asyncio.gather(*list_tasks, return_exceptions=True)
        print(f"[Main] Results={results}")

    time_taken_ms = (time.time()-start_time)*1000

    print(f"[Main] End! Time taken: {time_taken_ms:.2f} ms to run {N_TASKS} tasks.")


if __name__ == '__main__':
    asyncio.run(main())


"""
OUTPUT
------------------

[Main] Start
[Main] Preparing 10 tasks to be executed asynchronously...
[Main] Executing tasks asynchronously...
[HttpFetch::Task-1] Start - Getting data from 'https://dog.ceo/api/breeds/image/random'...
[HttpFetch::Task-2] Start - Getting data from 'https://dog.ceo/api/breeds/image/random'...
[HttpFetch::Task-3] Start - Getting data from 'https://dog.ceo/api/breeds/image/random'...
[HttpFetch::Task-4] Start - Getting data from 'https://dog.ceo/api/breeds/image/random'...
[HttpFetch::Task-5] Start - Getting data from 'https://dog.ceo/api/breeds/image/random'...
[HttpFetch::Task-6] Start - Getting data from 'https://dog.ceo/api/breeds/image/random'...
[HttpFetch::Task-7] Start - Getting data from 'https://dog.ceo/api/breeds/image/random'...
[HttpFetch::Task-8] Start - Getting data from 'https://dog.ceo/api/breeds/image/random'...
[HttpFetch::Task-9] Start - Getting data from 'https://dog.ceo/api/breeds/image/random'...
[HttpFetch::Task-10] Start - Getting data from 'https://dog.ceo/api/breeds/image/random'...
[HttpFetch::Task-3] End.
[HttpFetch::Task-7] End.
[HttpFetch::Task-8] End.
[HttpFetch::Task-4] End.
[HttpFetch::Task-2] End.
[HttpFetch::Task-9] End.
[HttpFetch::Task-1] End.
[HttpFetch::Task-6] End.
[HttpFetch::Task-10] End.
[HttpFetch::Task-5] End.
[Main] Results=[{'name': 'Task-1', 'response': {'status': 200, 'data': {'message': 'https://images.dog.ceo/breeds/poodle-miniature/n02113712_421.jpg', 'status': 'success'}}, 'time_taken_ms': 510.85}, {'name': 'Task-2', 'response': {'status': 200, 'data': {'message': 'https://images.dog.ceo/breeds/spaniel-welsh/n02102177_3928.jpg', 'status': 'success'}}, 'time_taken_ms': 505.68}, {'name': 'Task-3', 'response': {'status': 200, 'data': {'message': 'https://images.dog.ceo/breeds/bouvier/n02106382_4060.jpg', 'status': 'success'}}, 'time_taken_ms': 333.25}, {'name': 'Task-4', 'response': {'status': 200, 'data': {'message': 'https://images.dog.ceo/breeds/australian-shepherd/sadie.jpg', 'status': 'success'}}, 'time_taken_ms': 504.13}, {'name': 'Task-5', 'response': {'status': 200, 'data': {'message': 'https://images.dog.ceo/breeds/dhole/n02115913_2657.jpg', 'status': 'success'}}, 'time_taken_ms': 548.5}, {'name': 'Task-6', 'response': {'status': 200, 'data': {'message': 'https://images.dog.ceo/breeds/setter-english/n02100735_6658.jpg', 'status': 'success'}}, 'time_taken_ms': 527.08}, {'name': 'Task-7', 'response': {'status': 200, 'data': {'message': 'https://images.dog.ceo/breeds/komondor/n02105505_1148.jpg', 'status': 'success'}}, 'time_taken_ms': 360.22}, {'name': 'Task-8', 'response': {'status': 200, 'data': {'message': 'https://images.dog.ceo/breeds/retriever-golden/n02099601_176.jpg', 'status': 'success'}}, 'time_taken_ms': 401.65}, {'name': 'Task-9', 'response': {'status': 200, 'data': {'message': 'https://images.dog.ceo/breeds/shiba/shiba-6.jpg', 'status': 'success'}}, 'time_taken_ms': 506.24}, {'name': 'Task-10', 'response': {'status': 200, 'data': {'message': 'https://images.dog.ceo/breeds/havanese/00100trPORTRAIT_00100_BURST20191112123933390_COVER.jpg', 'status': 'success'}}, 'time_taken_ms': 535.65}]
[Main] End! Time taken: 552.51 ms to run 10 tasks.
"""
