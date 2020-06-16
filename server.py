from aiohttp import web
from functools import partial
import aiofiles
import argparse
import asyncio
import datetime
import logging
import os


async def archivate(request, parser_args):
    if parser_args.log:
        logging.basicConfig(level = logging.INFO)

    archive_hash = request.match_info.get('archive_hash')
    basic_path = parser_args.folder
    
    if not os.path.exists(basic_path + archive_hash):
        raise web.HTTPNotFound(text="Archive not exist or it has been deleted")

    cmd = ['zip', '-r', '-', archive_hash]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=basic_path,
    )

    response = web.StreamResponse()
    response.headers['Content-Type'] = 'application/zip'
    response.headers['Content-Disposition'] = 'form-data'

    await response.prepare(request)

    try:
        while True:
            stdout = await process.stdout.read(100*1024)
            if not stdout:
                await response.write_eof()
                break    
            
            logging.info(u'Sending archive chunk ...')
            await response.write(stdout)
            await asyncio.sleep(parser_args.delay)
    except asyncio.CancelledError:
        process.kill()
        await process.communicate()
        raise
    finally:
        return response
    

async def handle_index_page(request):
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', action='store_true', help="Activate debug-mode of logging")
    parser.add_argument('--delay', type=float, default=0, help="Delay of response")
    parser.add_argument('--folder', type=str, default='test_photos/', help="Directory with foto-files")
    archivate = partial(archivate, parser_args=parser.parse_args())
        
    app = web.Application(loop=asyncio.get_event_loop())
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archivate),
    ])
    web.run_app(app)

