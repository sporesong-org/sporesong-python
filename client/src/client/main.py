from client import Client
import asyncio

c = Client()

default_proxy_endpoint = "ws://localhost:4321"

async def main(target_proxy : str):
    while True:
        #try:
            connection_task = asyncio.create_task(c.client.connect(target_proxy))
            user_interface_task = asyncio.create_task(c.entry_point())
        
            await connection_task
        
        #except Exception:
        #    print(f"It seems that the proxy {target_proxy} is currently unreachable.")
        #    target_proxy = input("Enter another proxy address: ")

def connect_to_proxy():
    print(
    """
    Welcome to Sporesong.org!
    Before you get started, you'll need to connect to a proxy.

    Do you want to connect to the default proxy, or a specific one? (d/s)
    """)
    user_in : str = input()
    while not any(x in user_in for x in {"s", "d"}):
        print("Hm, I don't understand that input.")

    target_proxy = default_proxy_endpoint
    
    if "d" in user_in:
        pass
    elif "s" in user_in:
        target_proxy = input("Enter your proxy address: ")

    asyncio.run(main(target_proxy))

if __name__ == "__main__":
    connect_to_proxy()