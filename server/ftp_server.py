import socket
from time import sleep
from threading import Thread
import asyncio
import os
os.chdir('myfiles')

INTERFACE, SPORT = 'localhost', 8080
CHUNK = 100
CORRECT_PWD = "a\n"
PATH = os.getcwd()
LIST_FILES = "list"
PUT_FILE = "put"
GET_FILE = "get"
REMOVE_FILE = "remove"
CLOSE = "close"

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

async def handle_client(reader, writer):

    for i in range(3):
        await send_msg(writer, "Enter password: \n")               # 1
        pwd = await recv_msg(reader)                            # 2
        print("received " + pwd)
        if pwd == CORRECT_PWD:
            await send_msg(writer, "Welcome to the server.\n")     # 3a
            break
        else: 
            await send_msg(writer, "Incorrect password.\n")        # 3b

    if pwd != CORRECT_PWD:
        await send_msg(writer, "NAK Unable to connect to client: too many incorrect passwords.\n") 
        quit()
        
    while 1:
        await send_msg(writer, "ftp> \n")                       # 4
        input = await recv_msg(reader)                            # 5 
        fcn = input.split(" ",1)
        print("received " + str(fcn))
        
        if fcn[0] == LIST_FILES:    # List files in server's directory
            dir_list = os.listdir(PATH)
            await send_msg(writer, "ACK\n" + str(dir_list))         # 6

        elif fcn[0] == PUT_FILE:        # Uploads file from client to server
            file_to_put = fcn[1]
            print("to put: " + file_to_put)
            await send_msg(writer, "ACK\n")                 # 7a
            f = open(file_to_put, "w")
            file_contents = await recv_msg(reader)          # 7b
            f.write(file_contents)   
            f.close()                        

        elif fcn[0] == GET_FILE:    #Downloads file from server to client
            file_to_send = fcn[1]
            print("received " + file_to_send)
            check = os.path.isfile(file_to_send)
            if check: 
                await send_msg(writer, "ACK\n")                 # 8a
                with open(file_to_send, 'r') as send:
                    content = send.read()
                    await send_msg(writer, content)             # 8b
                    #file_to_send.close()
            else:
                await send_msg(writer, "NAK File does not exist.\n") 

        elif fcn[0] == REMOVE_FILE:     # Removes file on server
            if os.path.isfile(fcn[1]): 
                os.remove(fcn[1])  
                print("removed " + fcn[1])
                await send_msg(writer, "ACK\n")                             #9
            else:
                await send_msg(writer, "NAK File does not exist.\n")        #9

        elif fcn[0] == CLOSE:       # Closes server
            asyncio.get_event_loop().stop()                     # 10
            break

        else:
            await send_msg(writer, "Invalid function.\n")       # err
          
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
