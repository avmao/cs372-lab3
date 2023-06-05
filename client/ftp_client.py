import os
os.chdir('myfiles')

import socket
from time import sleep
from threading import Thread
import asyncio

IP, DPORT = 'localhost', 8080

def to_hex(number):
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

async def send_msg(writer, msg):
    writer.write(to_hex(len(msg)).encode())
    writer.write(msg.encode())

    await writer.drain()

async def recv_msg(reader: asyncio.StreamReader):
    data_length_hex = await reader.readexactly(8)
    data_length = int(data_length_hex, 16)

    full_data = await reader.readexactly(data_length)
    return full_data.decode()

async def connect(i):
    reader, writer = await asyncio.open_connection(IP, DPORT)

    for i in range(3):
        pwd_prompt = await recv_msg(reader)         # 1
        print(pwd_prompt.rstrip())
        pwd = input()
        await send_msg(writer, pwd+"\n")            # 2
        
        confirm = await recv_msg(reader)            # 3
        if confirm == "Welcome to the server.\n":
            break 
 
    print(confirm)

    func = ""

    while func != "close":
        func_prompt = await recv_msg(reader)            # 4
        print (func_prompt.strip() + " " , end="")
        func = input()
        command = func.split(" ")
        await send_msg(writer, func)   
        contents = await recv_msg(reader)
        print(contents)  
        if command[0] == "get":
            file_name = command[1]
            confirmfile = await recv_msg(reader)
            if confirmfile == "ACK\n":
                f = open(file_name, "w")
                file_contents = await recv_msg(reader)
                f.write(file_contents)   
                f.close()      
        elif command[0] == "put":
            file_to_put = command[1]
            check = os.path.isfile(file_to_put)
            if check: 
                with open(file_to_put, 'r') as send:
                    content = send.read()
                    await send_msg(writer, content)
                    #file_to_put.close()
            else:
                print("NAK File does not exist.\n")

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
