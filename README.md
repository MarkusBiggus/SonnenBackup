# SonnenBackup

Read from the real-time API on Sonnen Batterie to manage Backup Reserve capacity.

Readonly API, use Sonnen Batterie portal or mobile app to set Backup Reseve percent.

* Real time power, current and voltage
* Battery levels, Charge/Discharge rate, time to fully charged
* Backup reserve, time to reserve, time to fully discharged
* Temperature and batterie health

## Usage

`pip install sonnenbackup`

(will require sonnen_api_v2 driver package)


Then from within your project:

```
from sonnen_api_v2 import BatterieBackup, BatterieResponse,
import asyncio

async def validate():
    _batterie = BatterieBackup(auth_token, ip_address, port)
    return await _batterie.get_response()

async def update():
    _batterie = BatterieBackup(auth_token, ip_address, port)
    return await _batterie.get_response()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
response = loop.run_until_complete(update())
print(response)
```

## Confirmed Supported Batteries

These batteries have been tested and confirmed to be working. If your batterie is not listed below, this library may still work provided your battery admin portal can generate an API read token and responds to Sonnen API V2 endpoints.

* Power unit Evo IP56
