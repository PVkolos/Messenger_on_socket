from Socket import Socket
from ex import SocketException


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        self.users = []

    def set_up(self):
        self.socket.bind(('localhost', 5001))
        self.socket.listen()
        self.socket.setblocking(False)

    async def send_data(self, **kwargs):
        for user in self.users:
            try:
                await super(Server, self).send_data(where=user, message=kwargs['message'])
            except SocketException:
                user.close()
                return

    async def listen_socket(self, user):
        while True:
            try:
                data = await super(Server, self).listen_socket(user)
                await self.send_data(message=data['message'])
            except SocketException:
                user.close()
                return
            print(f'User send {data["message"]}')

    async def start_server(self):
        while True:
            socket_user, address = await self.main_loop.sock_accept(self.socket)
            print(f'Connected user {socket_user}')
            self.users.append(socket_user)
            self.main_loop.create_task(self.listen_socket(socket_user))

    async def main(self):
        await self.main_loop.create_task(self.start_server())

    def start(self):
        self.main_loop.run_until_complete(self.main())


if __name__ == '__main__':
    server = Server()
    server.set_up()
    server.start()
