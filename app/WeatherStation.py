#!venv/bin/python
import sys
import json
import re
import aiohttp
import asyncio
import bs4
import time
import hashlib

source_url = 'http://metservice.intnet.mu/latest-weather-data.php';
WeatherDataArray = [];
WeatherCategoryMap = {
    '3hrRainfall': "rain",
    'Max&MinTemp': "temperature",
    'Wind': "wind",
    'Humidity': "humidity"
}

UpdateInterval = {
    1: True,
    4: True,
    7: True,
    10: True,
    13: True,
    16: True,
    19: True,
    22: True
}

# Load Previous MD5
old_hash_object= open("md5.txt","r").read()

file= open("md5.txt","w+")

async def bs4Response(html):
    soup = bs4.BeautifulSoup(html, 'lxml');

    for WeatherDataTabs in soup.findAll('ul', {'class': 'tabs'}):
        for tab in WeatherDataTabs.findAll('li'):
            if tab.get_text()!="24 hr Rainfall":
                WeatherDataID = tab.a.attrs.get('href').replace("#", "");

                for WeatherData in soup.findAll('div', {'id': WeatherDataID}):
                    for Station in WeatherData.findAll('div', {'class', 'station'}):
                        WeatherUUID = "";

                        if tab.get_text()=="3 hr Rainfall":
                            WeatherUUIDTemp= WeatherData.find('div', {'class': 'weatherinfo'})
                            WeatherUUID= re.sub(r'\s', '', WeatherUUID.p.get_text().replace(" ", ""))

                        item = {
                            "region": Station.attrs.get('title'),
                            "value": re.sub(r'\s', '', Station.p.get_text()),
                            "category": WeatherCategoryMap[tab.get_text().replace(" ", "")],
                            "country": "Mauritius",
                            "recorded_date": "",
                            "UUID": WeatherUUID
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
    new_hash_object = hashlib.md5(json.dumps(WeatherDataArray).encode('utf-8'));

    if old_hash_object != new_hash_object.hexdigest():
        for i in range(len(WeatherDataArray)):
            WeatherDataArray[i]['recorded_date'] = time.time();
            
        async with aiohttp.ClientSession() as session:
            async with session.post('http://127.0.0.1:3000/api/observation', json=WeatherDataArray) as resp:
                print(resp)
                file.write(new_hash_object.hexdigest());
    else:
        print('no change')
        file.write(old_hash_object);

loop = asyncio.get_event_loop()
tasks = [  
    asyncio.ensure_future(fetchData(source_url)),
]
loop.run_until_complete(asyncio.wait(tasks))
loop.run_until_complete(saveData())
loop.close()
    
