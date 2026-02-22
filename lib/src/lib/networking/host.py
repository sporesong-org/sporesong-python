"""
Author: Orion Hess
Created: 2026-02-21
Edited: 2026-02-21
Purpose: Code for the proxy listening on a port and responding to connections
"""
import socket

def get_listener(bind_address: str, port: int, connections: int) -> socket.socket:
    """
    Get a listening socket
    :param bind_address: Address to bind to
    :param port: Port to listen on
    :param connections: Number of connections to queue
    :return: Listening socket
    """
    s = socket.socket()
    print("Socket created")

    s.bind((bind_address, port))
    print(f"Socket bound to port: {port} on '{bind_address}'")

    s.listen(connections)

    return s
