import asyncio
import websockets

async def handle_connection(websocket, path):
    try:
        # SSH Port 22 ကို ချိတ်ဆက်ခြင်း
        reader, writer = await asyncio.open_connection('127.0.0.1', 22)
        
        # Connection အောင်မြင်ကြောင်း Client ကို အကြောင်းကြားခြင်း
        await websocket.send("HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n\r\n")

        async def ws_to_ssh():
            try:
                async for msg in websocket:
                    writer.write(msg)
                    await writer.drain()
            except: pass
            finally: writer.close()

        async def ssh_to_ws():
            try:
                while True:
                    data = await reader.read(4096)
                    if not data: break
                    await websocket.send(data)
            except: pass
            finally: await websocket.close()

        await asyncio.gather(ws_to_ssh(), ssh_to_ws())
    except:
        pass

start_server = websockets.serve(handle_connection, "0.0.0.0", 80) # Port 80 မှာ run မည်
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
