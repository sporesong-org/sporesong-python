import asyncio
from lib.networking import server
from websockets.asyncio.server import ServerConnection
import time


async def print_stuff(socket: ServerConnection, message):
    print(socket.id, message)
    await s.id_to_connection[socket.id].put(str(socket.id))

async def tx(socket: ServerConnection, message):
    await socket.send(message, text=True)

s = server.Server(print_stuff, tx)

async def main():
    await s.start_server("", 4321)


if __name__ == "__main__":
    asyncio.run(main())
