import asyncio
from threading import Thread

def _AsyncLoop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def StartAsyncLoop():
    ASYNC_LOOP = asyncio.new_event_loop()
    t = Thread(target=_AsyncLoop, args=(ASYNC_LOOP,))
    t.start()
    return (t, ASYNC_LOOP)