import socket
from time import sleep
from threading import Thread
import asyncio
import os
os.chdir('myfiles')

INTERFACE, SPORT = 'localhost', 8080
CHUNK = 100
CORRECT_PWD = "lab3cs372\n"

async def send_short_msg(writer, msg):
    writer.write(msg.encode())
    await writer.drain()

async def recv_pwd(reader: asyncio.StreamReader):
    full_data = await reader.readline()
    return full_data.decode()

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

    print("Do server stuff")

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
