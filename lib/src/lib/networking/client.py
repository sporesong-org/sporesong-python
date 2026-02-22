"""
Author: Orion Hess
Created: 2026-02-21
Edited: 2026-02-21
Purpose: Class to connect to a server, receive, and send messages
"""

import asyncio
from typing import Callable
from websockets.asyncio.client import ClientConnection, connect

class Client:
    def __init__(self, function_rx: Callable, function_tx: Callable):
        """
        Create a client object to connect to a server. Send messages by adding them to the watch_tx queue
        :param function_rx: Function to call for received packets - must take (message: str)
        :param function_tx: Function to call for outbound packets - must take (socket: ClientConnection, message: str)
        """
        self.function_rx = function_rx
        self.function_tx = function_tx
        self.watch_tx = asyncio.Queue()
        
    async def __client_rx(self, websocket: ClientConnection):
        async for message in websocket:
            await self.function_rx(message)

    async def __client_tx(self, websocket: ClientConnection):
        while True:
            message = await self.watch_tx.get()
            await self.function_tx(websocket, message)

    async def connect(self, uri: str):
        """
        Connect to a server with it's URI
        :param uri: String URI 'ws://hostname:port'
        """
        async with connect(uri) as websocket:
            await asyncio.gather (
                self.__client_rx(websocket),
                self.__client_tx(websocket),
            )