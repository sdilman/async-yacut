import os
import urllib

import aiohttp
import asyncio


API_HOST = os.getenv('API_HOST', 'https://cloud-api.yandex.net/')
API_VERSION = os.getenv('API_VERSION', 'v1')
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
DISK_TOKEN = os.getenv('DISK_TOKEN', 'your token')
AUTH_HEADERS = {
    'Authorization': f'OAuth {DISK_TOKEN}'
}


async def async_upload_files(images):
    if images is not None:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for image in images:
                tasks.append(
                    asyncio.ensure_future(
                        async_process_file(session, image)
                    )
                )
            urls = await asyncio.gather(*tasks)
        return urls


async def async_process_file(session, image):
    payload = {
        'path': f'app:/{image.filename}',  # noqa E231
        'overwrite': 'True'
    }

    async with session.get(
        headers=AUTH_HEADERS,
        params=payload,
        url=REQUEST_UPLOAD_URL
    ) as response:
        response_serialized = await response.json()
        upload_url = response_serialized['href']

    async with session.put(
        data=image.read(),
        url=upload_url,
    ) as response:
        response_headers = response.headers
        location = urllib.parse.unquote(
            response_headers['Location']
        ).replace('/disk', '')

    async with session.get(
        headers=AUTH_HEADERS,
        url=DOWNLOAD_LINK_URL,
        params={'path': location}
    ) as response:
        response_serialized = await response.json()
        return response_serialized['href']
