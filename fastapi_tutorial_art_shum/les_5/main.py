from fastapi import FastAPI, BackgroundTasks
import time
import asyncio


app = FastAPI()


def sync_task():
    time.sleep(3)
    print("Email отправлен")


# длинная задача, мы не хотим, чтобы она тормозила всё остальное, сделаем её фоновой
async def async_task():
    await asyncio.sleep(3)
    print("Был сделан запрос на сторонний API")


@app.post("/")
async def some_route(background_tasks: BackgroundTasks):
    ...
    # asyncio.create_task(async_task())
    background_tasks.add_task(sync_task)
    return {"ok": True}
