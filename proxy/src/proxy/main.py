from proxy import Proxy
import asyncio

p = Proxy()

async def main():
    await p.host.start_server("", 4321)

if __name__ == "__main__":
    asyncio.run(main())