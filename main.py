import asyncio
from datetime import datetime
import googlemaps
from timeit import default_timer
from aiohttp import ClientSession
from pytile import async_login
import bleak

import config

async def maps() -> None:
    gmaps = await googlemaps.Client(key="AIzaSyDlMzYGce3b7aTDSsKNEvdXe7Qf7ouoHMI")
    geocode_from = gmaps.geocode("7006 SE 72nd Ave Portland, OR 97206 United States")
    geocode_to = gmaps.geocode("1825 SW Broadway Portland, OR 97201 United States")
    now = datetime.now()
    directions_result = gmaps.directions("", "", mode="transit", departure_time=now)

async def login_to_tile(username: str, password: str) -> None:
    async with ClientSession() as session:
        api = await async_login(username, password, session)
        tiles = await api.async_get_tiles()
        for uuid, tile in tiles.items():
            print("Tile UUID", uuid)
            print("Tile Name", tile.name)
            print()

def time_to_seconds(time_hr: int = 0, time_min: int = 0, time_sec: int = 0) -> int:
    return (60 * ((time_hr * 60) + time_min)) + time_sec

async def look_for_devices(time_limit: int, percentage: int, interval: int = 5):
    device_list_per_interval: [set(bleak.BLEDevice)] = []
    start_time = default_timer()
    while (default_timer() - start_time) < time_limit:
        devices = await bleak.BleakScanner.discover(timeout=interval)
        device_list_per_interval.append(set(devices))
    results: set(bleak.BLEDevice) = set()
    for go in device_list_per_interval:
        for device in go:
            results.add(device)
    print("Devices:")
    for d in results:
        print(d.name, d.address)
        print(d.details)
        print()

    # devices_of_concern

config = config.get_config()
asyncio.run(look_for_devices(1, 90))
