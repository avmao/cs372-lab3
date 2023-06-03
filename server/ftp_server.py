import socket
from time import sleep
from threading import Thread
import asyncio
import os
os.chdir('myfiles')

INTERFACE, SPORT = 'localhost', 8080
CHUNK = 100
CORRECT_PWD = "lab3cs372\n"
PATH = os.getcwd()
LIST_FILES = "list\n"
PUT_FILE = "put file\n"
GET_FILE = "get file\n"
REMOVE_FILE = "remove file\n"
CLOSE = "close\n"

async def send_short_msg(writer, msg):
    writer.write(msg.encode())
    await writer.drain()

async def recv_pwd(reader: asyncio.StreamReader):
    full_data = await reader.readline()
    return full_data.decode()

async def recv_func(reader: asyncio.StreamReader):
    which_function = await reader.readline()
    return which_function.decode()

async def put_func(reader: asyncio.StreamReader):
    print("Put")

async def get_func(reader: asyncio.StreamReader):
    print("Get")

async def remove_func(reader: asyncio.StreamReader):
    print("Remove")

async def handle_client(reader, writer):

    for i in range(3):
        await send_short_msg(writer, "Enter password:\n")        # 1
        pwd = await recv_pwd(reader)                            # 2
        print("received " + pwd)
        if pwd == CORRECT_PWD:
            await send_short_msg(writer, "Welcome to the server.\n")     # 3a
            break
        else: 
            await send_short_msg(writer, "Incorrect password.\n")        # 3b

    if pwd != CORRECT_PWD:
        await send_short_msg(writer, "NAK Unable to connect to client: too many incorrect passwords.\n") 
        quit()

    await send_short_msg(writer, "What function to perform?\n")
    fcn = await recv_func(reader)    
    print("received " + fcn)
          
    if fcn == LIST_FILES:
        #dir_list = os.listdir(PATH)
        #await send_short_msg(writer, "ACK ")
        #printlist = print(dir_list)
        #await send_short_msg(writer, printlist)
        print("test")
    elif fcn == PUT_FILE:
        put_func(reader)
    elif fcn == GET_FILE:
        get_func(reader)
    elif fcn == REMOVE_FILE:
        remove_func(reader) 
    elif fcn == CLOSE:
        writer.close()
    else:
         await send_short_msg(writer, "Invalid function.\n")
          
    writer.close()
    await writer.wait_closed()


async def main():
    print("Starting the server")
    server = await asyncio.start_server(
        handle_client,
        INTERFACE, SPORT
    )

    async with server:
        await server.serve_forever()

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())
