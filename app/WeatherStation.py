#!venv/bin/python
import sys
import json
import re
import aiohttp
import asyncio
import bs4
import time
   
source_url = 'http://metservice.intnet.mu/latest-weather-data.php';
WeatherDataArray = [];
WeatherCategoryMap = {
    '3hrRainfall': "rain",
    'Max&MinTemp': "temperature",
    'Wind': "wind",
    'Humidity': "humidity"
}

async def bs4Response(html):
    soup = bs4.BeautifulSoup(html, 'lxml');

    for WeatherDataTabs in soup.findAll('ul', {'class': 'tabs'}):
        for tab in WeatherDataTabs.findAll('li'):
            if tab.get_text()!="24 hr Rainfall":
                WeatherDataID = tab.a.attrs.get('href').replace("#", "");

                for WeatherData in soup.findAll('div', {'id': WeatherDataID}):
                    for Station in WeatherData.findAll('div', {'class', 'station'}):
                        item = {
                            "region": Station.attrs.get('title'),
                            "value": re.sub(r'\s', '', Station.p.get_text()),
                            "category": WeatherCategoryMap[tab.get_text().replace(" ", "")],
                            "country": "Mauritius",
                            "recorded_date": time.time(),
                        };

                        WeatherDataArray.append(item);
                        

async def fetch(session, url):
     async with session.get(url) as response:
        return await response.text()
    

async def fetchData(url):
    print('Starting {}'.format(url))

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        await bs4Response(html)
        print('Ending {}'.format(url))

async def saveData():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:3000/api/observation', json=WeatherDataArray) as resp:
            print(resp)


loop = asyncio.get_event_loop()
tasks = [  
    asyncio.ensure_future(fetchData(source_url)),
]
loop.run_until_complete(asyncio.wait(tasks))
loop.run_until_complete(saveData())
loop.close()
    
