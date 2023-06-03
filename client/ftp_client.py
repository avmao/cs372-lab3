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

async def send_pwd(writer, pwd):
    writer.write(pwd.encode())
    await writer.drain()

async def send_func(writer, func):
    writer.write(func.encode())
    await writer.drain()

async def connect(i):
    reader, writer = await asyncio.open_connection(IP, DPORT)

    for i in range(3):
        pwd_prompt = await recv_short_msg(reader)       # 1
        print(pwd_prompt)
        pwd = input()
        await send_pwd(writer, pwd+"\n")                     # 2
        
        confirm = await recv_short_msg(reader)          # 3
        if confirm == "Welcome to the server.\n":
            break 
 
    print(confirm)
    while confirm != "Close":
        func_prompt = await recv_short_msg(reader)
        print (func_prompt)
        func = input()
        await send_func(writer, func+"\n")
        confirm = await recv_short_msg(reader)

    return 0

async def main():
    tasks = []
    for i in range(1):
        tasks.append(connect(str(i).rjust(8, '0')))

    await asyncio.gather(*tasks)
    print("done")

if __name__ == "__main__":
    #asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
