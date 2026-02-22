import lib.networking.client
from server import Server
import asyncio

s = Server()

async def starting() -> None:
    conenction_task = asyncio.create_task(s.client.connect("ws://pacific:4321"))
    boot_task = asyncio.create_task(s.boot())
    await conenction_task
    
    

if __name__=="__main__":
    asyncio.run (starting())