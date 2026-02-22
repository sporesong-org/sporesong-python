import asyncio
from lib.networking import server
from websockets.asyncio.server import ServerConnection
import time

def print_stuff(message):
    print(message)

async def tx(socket: ServerConnection, message):
    await socket.send(message)


async def main():
    s = server.Server(print_stuff, tx)
    await s.start_server("", 4321)


if __name__ == "__main__":
    asyncio.run(main())
