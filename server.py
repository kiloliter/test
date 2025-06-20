import asyncio
import os
import websockets

clients = set()

# Health check support for Render
async def process_request(path, request_headers):
    if path == "/":
        return (
            200,
            [("Content-Type", "text/plain")],
            b"OK\n"
        )
    return None  # Let websockets handle the rest

# WebSocket message handler
async def handle_client(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")
            # Echo message to all connected clients
            for client in clients.copy():
                if client.open:
                    await client.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

async def main():
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting WebSocket server on port {port}")
    async with websockets.serve(
        handle_client,
        host="0.0.0.0",
        port=port,
        process_request=process_request,
    ):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
