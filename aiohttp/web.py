from aiohttp import web
from asyncio import sleep

async def wait(req: web.Request) -> web.Response:
    await sleep(1)
    return web.json_response(r"{\"hello\": \"world\"}")

if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.get("/wait", wait)
    ])
    web.run_app(app, host="localhost", port=8000)