import socket
import asyncio


class Socket:
    def __init__(self):
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        self.main_loop = asyncio.new_event_loop()

    async def send_data(self, **kwargs):
        where = kwargs['where']
        data = kwargs['data']
        del kwargs['where']
        del kwargs['data']
        await self.main_loop.sock_sendall(where, data)

    async def listen_socket(self, listened_socket):
        pass
