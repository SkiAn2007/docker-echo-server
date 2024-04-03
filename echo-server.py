#!/usr/bin/env python3

import platform
import asyncio

PORT_ECHO_UDP_1 = 4001
PORT_ECHO_UDP_2 = 4002
PORT_ECHO_UDP_3 = 4003
PORT_ECHO_TCP_1 = 5001
PORT_ECHO_TCP_2 = 5002
PORT_ECHO_TCP_3 = 5003
INADDR_ANY = "0.0.0.0"

SERVER_NAME = platform.node()


class UdpEchoServer:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        in_msg = data.decode().strip()
        print(f'UDP: Received {in_msg} from {addr}')
        out_msg = f'UDP: {SERVER_NAME} received: {in_msg}\n'
        self.transport.sendto(out_msg.encode(), addr)


class TcpEchoServer(asyncio.Protocol):
    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        print(f'TCP: Connection from {self.peername}')
        self.transport = transport

    def data_received(self, data):
        in_msg = data.decode().strip()
        print(f'TCP: Received: {in_msg} from {self.peername}')
        out_msg = f'TCP: {SERVER_NAME} received: {in_msg}\n'
        self.transport.write(out_msg.encode())


async def main():
    loop = asyncio.get_running_loop()

    print(f"Starting UDP server on port {PORT_ECHO_UDP_1}")
    await loop.create_datagram_endpoint(
        lambda: UdpEchoServer(),
        local_addr=(INADDR_ANY, PORT_ECHO_UDP_1))

    print(f"Starting UDP server on port {PORT_ECHO_UDP_2}")
    await loop.create_datagram_endpoint(
        lambda: UdpEchoServer(),
        local_addr=(INADDR_ANY, PORT_ECHO_UDP_2))

    print(f"Starting UDP server on port {PORT_ECHO_UDP_3}")
    await loop.create_datagram_endpoint(
        lambda: UdpEchoServer(),
        local_addr=(INADDR_ANY, PORT_ECHO_UDP_3))

    print(f"Starting TCP server on port {PORT_ECHO_TCP_1}")
    tcp_server_1 = await loop.create_server(
        lambda: TcpEchoServer(),
        INADDR_ANY, PORT_ECHO_TCP_1)

    print(f"Starting TCP server on port {PORT_ECHO_TCP_2}")
    tcp_server_2 = await loop.create_server(
        lambda: TcpEchoServer(),
        INADDR_ANY, PORT_ECHO_TCP_2)

    print(f"Starting TCP server on port {PORT_ECHO_TCP_3}")
    tcp_server_3 = await loop.create_server(
        lambda: TcpEchoServer(),
        INADDR_ANY, PORT_ECHO_TCP_3)

    async with tcp_server_1:
        await tcp_server_1.serve_forever()

    async with tcp_server_2:
        await tcp_server_2.serve_forever()

    async with tcp_server_3:
        await tcp_server_3.serve_forever()

asyncio.run(main())
