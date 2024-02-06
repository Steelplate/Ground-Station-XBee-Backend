import websockets
from websockets import WebSocketClientProtocol
from threading import Thread
from time import sleep
import asyncio

class WebSocket:
    def __init__(self, ip: str, port: int):
        self.ip: str = ip;
        self.port: str = port;

        self._socket: WebSocketClientProtocol = None
        self._thread: Thread = None

        self.should_stop: bool = False
        self.is_running: bool = False

        self._message_queue: list = []

    def run(self) -> None:
        self._thread = Thread(target=lambda: asyncio.run(self._run()))
        self._thread.start()
        print("Started socket")

    def stop(self) -> None:
        self.should_stop = True

        while self.is_running:
            pass

        print("Stopped socket")

    def send_data(self, data: str) -> None:
        self._message_queue.append(data)

    async def _connect_socket(self) -> WebSocketClientProtocol:
        socket: WebSocketClientProtocol = None
        try:
            socket = await websockets.connect(f"wss://{self.ip}:{self.port}", extra_headers={"backend-password": "PASSWORD"})
        except Exception as e:
            print(type(e))
            print(e)

        return socket

    async def _run(self) -> None:
        self.is_running = True

        self._socket = await self._connect_socket()
        
        while not self.should_stop:
            if(len(self._message_queue) > 0):
                await self._socket.send(self._message_queue.pop(0))

        self.is_running = False


        
