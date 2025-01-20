# SonnenBackup

Read from the real-time API on Sonnen Batterie to manage Backup Reserve capacity.

Readonly API, use Sonnen Batterie portal or mobile app to set Backup Reserve percent.

* System state On Grid, Off Grid or Critical Error.
* Real time power, current and voltage
* Battery levels, Charge/Discharge rate, time to fully charged
* Backup reserve, time to reserve, time to fully discharged
* Temperature and batterie health

## HACS

Install SonnenBackup integration.

## Usage

# install sonnenbackup with hacs

(requires sonnen_api_v2 driver package)


## Confirmed Supported Batteries

These batteries have been tested and confirmed to be working. If your batterie is not listed below, this library may still work provided your battery admin portal can generate an API read token and responds to Sonnen API V2 endpoints.

* Power unit Evo IP56
