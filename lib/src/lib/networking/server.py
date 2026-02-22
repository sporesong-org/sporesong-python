"""
Author: Orion Hess
Created: 2026-02-21
Edited: 2026-02-21
Purpose: Class to start a listening server, receive, and send messages
"""

import asyncio
from typing import Callable
import websockets
from websockets.asyncio.server import ServerConnection, serve

class Server:
    def __init__(self, function_rx: Callable, function_tx: Callable):
        """
        Create a serve object to listen on a port. Send messages by adding them to the watch_tx queue
        :param function_rx: Function to call for received packets - must take (message: str)
        :param function_tx: Function to call for outbound packets - must take (socket: ClientConnection, message: str)
        """
        self.function_rx = function_rx
        self.function_tx = function_tx
        self.watch_tx = asyncio.Queue()
        self.server = None
        
    async def __server_rx(self, websocket: ServerConnection):
        async for message in websocket:
            self.function_rx(message)
            await self.function_tx(websocket, "mic check 6 7 ")

    async def __server_tx(self, websocket: ServerConnection):
        while True:
            message = await self.watch_tx.get()
            await self.function_tx(websocket, message)

    async def server_connection_handler(self, websocket: ServerConnection) -> None:
        print(f"Client connected from {websocket.remote_address}")
        try:
            await asyncio.gather (
                self.__server_rx(websocket),
                self.__server_tx(websocket),
            )
        except websockets.exceptions.ConnectionClosed:
            print(f"Client on '{websocket.remote_address}' disconnected")


    async def start_server(self, bind_address: str, port: int):
        async with serve(self.server_connection_handler, bind_address, port) as server:
            self.server = server
            print(f"Server listening on port: {port} bound to address: {bind_address}")
            await server.serve_forever()