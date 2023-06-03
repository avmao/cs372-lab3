import socket
from time import sleep
from threading import Thread
import asyncio
import os
os.chdir('myfiles')

INTERFACE, SPORT = 'localhost', 8080
CHUNK = 100
CORRECT_PWD = "lab3cs472"

async def short_msg(writer, msg):
    writer.write(msg.encode())
    await writer.drain()

async def recv_pwd(reader: asyncio.StreamReader):
    full_data = await reader.readline()
    return full_data.decode()

async def handle_client(reader, writer):
    count = 1
    pwd = ""

    while pwd != "lab3cs472":
        if count > 3:
            await short_msg(writer, "NAK: Unable to connect to client.\n")
            quit()

        await short_msg(writer, "Enter password: ")
        recv_pwd(reader)
        count+=1

    short_msg(writer, "Welcome to the server.\n")

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(
        handle_client,
        INTERFACE, SPORT
    )

    async with server:
        await server.serve_forever()

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())
