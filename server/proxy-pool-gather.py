# proxy-pool-gather.py
import asyncio

import redis
from proxybroker import Broker
import logging

# logging.basicConfig(level=logging.DEBUG)


print("Start")
r = redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
print("Redis connected")


async def save(proxies):
    while True:
        proxy = await proxies.get()
        if proxy is None:
            break
        proto = 'https' if 'HTTPS' in proxy.types else 'http'
        row = '%s://%s:%d' % (proto, proxy.host, proxy.port)
        print("找到了：" + row)
        r.set(row, 1)
        print("保存了：" + r.get(row))


async def show(proxies):
    while True:
        proxy = await proxies.get()
        if proxy is None:
            break
        print('Found proxy: %s' % proxy)


def main():
    print("Getting proxies")

    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=['HTTP', 'HTTPS'], limit=10000, verify_ssl=False), save(proxies)
    )

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(tasks)
    except asyncio.TimeoutError:
        print("RETRYING PROXIES ...")


if __name__ == '__main__':
    main()