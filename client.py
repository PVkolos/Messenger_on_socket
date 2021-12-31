import asyncio
from Socket import Socket


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        self.messages = ""

    def set_up(self):
        try:
            self.socket.connect(('localhost', 5001))
        except ConnectionRefusedError:
            print("Sorry, server is offline")
            exit(0)
        self.socket.setblocking(False)

    async def listen_socket(self, listened_socket):
        while True:
            data = await self.main_loop.sock_recv(listened_socket, 4096)
            print(data.decode('utf-8'))

    async def send_data(self):
        while True:
            message = await self.main_loop.run_in_executor(None, input, ":::")
            await super(Client, self).send_data(where=self.socket, data=message.encode('utf-8'))

    async def main(self):
        await asyncio.gather(
            self.main_loop.create_task(self.listen_socket(self.socket)),
            self.main_loop.create_task(self.send_data())
        )

    def start(self):
        self.main_loop.run_until_complete(self.main())


if __name__ == '__main__':
    client = Client()
    client.set_up()
    client.start()