import asyncio
import os
import websockets

connected = set()

async def handler(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")
            for conn in connected:
                await conn.send(f"Echo: {message}")
    finally:
        connected.remove(websocket)

async def main():
    port = int(os.environ.get("PORT", 5000))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"Listening on port {port}...")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
