#!venv/bin/python
import sys
import json
import re
import aiohttp
import asyncio
import bs4
import time
import hashlib
import os
import json
import Config

source_url = 'http://metservice.intnet.mu/synoptic-chart.php';
metadata = {
    "Filename": "",
    "FilePath": "",
    "ExternalSource": True,
    "FileType": "SYNOPTIC_CHART",
};

async def bs4Response(html):
    soup = bs4.BeautifulSoup(html, 'lxml');

    for leftContent in soup.findAll('div', {'class': 'left_content'}):
        for image in leftContent.findAll('img'):
            metadata['Filename'] = "SYNOPTIC_CHART_" + os.path.basename(image['src']);
            metadata['FilePath'] = image['src'];

async def fetch(session, url):
     async with session.get(url) as response:
        return await response.text()
    
async def fetchPage(url):
    print('Starting {}'.format(url))

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        await bs4Response(html)
        print('Ending {}'.format(url))

async def saveData():
    async with aiohttp.ClientSession() as session:
        async with session.get(Config.Host + '/DocumentMetadata?filter[Filename]=' + metadata['Filename']) as resp:
            response = await resp.read();
            response = json.loads(response);

            if response['size'] == 0:
                async with session.post(Config.Host + '/DocumentMetadata', json=metadata) as resp:
                    print(resp)
        
        

def Run():
    loop = asyncio.get_event_loop()
    tasks = [  
        asyncio.ensure_future(fetchPage(source_url)),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.run_until_complete(saveData())
    loop.close()

Run()

