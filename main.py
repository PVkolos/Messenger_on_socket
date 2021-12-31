from Socket import Socket


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        self.users = []

    def set_up(self):
        self.socket.bind(('localhost', 5001))
        self.socket.listen()
        self.socket.setblocking(False)

    async def send_data(self, data):
        for user in self.users:
            await super(Server, self).send_data(where=user, data=data)

    async def listen_user(self, user):
        while True:
            data = await self.main_loop.sock_recv(user, 4096)
            print(f'User send {data}')
            await self.send_data(data)

    async def start_server(self):
        while True:
            socket_user, address = await self.main_loop.sock_accept(self.socket)
            self.users.append(socket_user)
            self.main_loop.create_task(self.listen_user(socket_user))

    async def main(self):
        await self.main_loop.create_task(self.start_server())

    def start(self):
        self.main_loop.run_until_complete(self.main())


if __name__ == '__main__':
    server = Server()
    server.set_up()
    server.start()
