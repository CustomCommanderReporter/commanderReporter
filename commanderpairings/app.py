import asyncio
from pathlib import Path
from aiohttp import web
import jinja2
import aiohttp_jinja2
from .routes import setup_routes

async def create_app():
    app = web.Application()
    app.router.add_static('/src', Path('./commanderpairings/src'))
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('commanderpairings', 'templates')
    )
    setup_routes(app)
    return app
