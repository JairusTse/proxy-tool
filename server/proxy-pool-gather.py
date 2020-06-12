# proxy-pool-gather.py
import asyncio

import redis
from proxybroker import Broker
import logging

# logging.basicConfig(level=logging.DEBUG)


print("Start")
r = redis.Redis(host='localhost', db=2, encoding="utf-8", decode_responses=True)
print("Redis connected")


async def save(proxies):
    while True:
        proxy = await proxies.get()
        if proxy is None:
            break
        print(proxy)
        if "HTTP" not in proxy.types:
            continue
        if "High" == proxy.types["HTTP"]:
            row = '%s://%s:%d' % ("http", proxy.host, proxy.port)
            r.set(row, 0, ex=60 * 60 * 24)


async def show(proxies):
    while True:
        proxy = await proxies.get()
        if proxy is None:
            break
        print('Found proxy: %s' % proxy)


def main():
    print("Getting proxies")
    # proxies = asyncio.Queue()
    # broker = Broker(proxies, timeout=2, max_tries=2, grab_timeout=3600)
    # tasks = asyncio.gather(broker.find(types=['HTTP', 'HTTPS']),
    #                        save(proxies))
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(tasks)

    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=['HTTP', 'HTTPS'], limit=10, verify_ssl=False), show(proxies)
    )

    try:
        loop = asyncio.get_event_loop()
        # loop.run_until_complete(asyncio.wait_for(tasks, 30))
        loop.run_until_complete(tasks)
    except asyncio.TimeoutError:
        print("RETRYING PROXIES ...")

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(tasks)


if __name__ == '__main__':
    main()