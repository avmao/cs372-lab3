import os
os.chdir('myfiles')

import socket
from time import sleep
from threading import Thread
import asyncio

IP, DPORT = 'localhost', 8080

async def recv_short_msg(reader: asyncio.StreamReader):
    full_data = await reader.readline()
    return full_data.decode()

async def send_pwd(writer):
    pwd = input()

    writer.write(pwd.encode())
    await writer.drain()

async def connect(i):
    reader, writer = await asyncio.open_connection(IP, DPORT)

    intro = await recv_short_msg(reader)
    print(intro)

    while recv_short_msg(reader) != "Welcome to the server.\n":
        recv_short_msg(reader)
        await send_pwd(writer)


    return 0

async def main():
    tasks = []
    for i in range(100):
        tasks.append(connect(str(i).rjust(8, '0')))

    await asyncio.gather(*tasks)
    print("done")

if __name__ == "__main__":
    #asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
