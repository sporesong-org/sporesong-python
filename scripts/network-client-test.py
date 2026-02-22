import asyncio
from lib.networking import client
from websockets.asyncio.client import ClientConnection

def print_stuff(message):
    print(message)

async def tx(socket: ClientConnection, message):
    await socket.send(message)

c = client.Client(print_stuff, tx)

async def main():
    await c.watch_tx.put("mic check 3 4")
    await c.connect("ws://localhost:4321")



if __name__ == "__main__":
    asyncio.run(main())
