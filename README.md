# SonnenBackup

Read from the real-time API on Sonnen Batterie to manage Backup Reserve capacity.

Readonly API, use Sonnen Batterie portal or mobile app to set Backup Reserve percent.

* System state On Grid, Off Grid or Critical Error.
* Real time power, current and voltage
* Battery levels, Charge/Discharge rate, time to fully charged
* Backup reserve, time to reserve, time to fully discharged
* Temperature and batterie health

Uses sonnen_api_v2 driver package which requires a readonly API Token created in the
device management portal.

## HACS

Install SonnenBackup integration.


## Usage

install sonnenbackup with hacs

### Sensors
```
Package Sensor	Unit	alias	hass sensor
status_backup_buffer	percent		status_backup_buffer
led_state	string		led_state
system_status	string		system_status
battery_activity_state	string	 sonnenbackup_state	 sonnenbackup_state
battery_cycle_count	integer		battery_cycle_count
battery_full_charge_capacity_wh	kWh	 full_charge_capacity	 full_charge_capacity
status_remaining_capacity_wh	kWh	 remaining_capacity	 remaining_capacity
capacity_until_reserve	kWh		capacity_until_reserve
backup_buffer_capacity_wh	kWh	 backup_reserve_capacity	 backup_reserve_capacity
status_usable_capacity_wh	kWh	 usable_remaining_capacity	 usable_remaining_capacity
kwh_consumed	kWh		kwh_consumed
kwh_produced	kWh		kwh_produced
consumption_average 	watts		consumption_average
status_frequency	hertz	 frequency	 frequency
status_rsoc	percent	 relative_state_of_charge	 relative_state_of_charge
status_usoc	percent	 usable_state_of_charge	 usable_state_of_charge
consumption_total_w	watts	 consumption_daily	 consumption_daily
production_total_w	watts	 production_daily	 production_daily
consumption	watts	 consumption_now	 consumption_now
production	watts	 production_now	 production_now
inverter_pac_total	watts	 ongrid_pac	 ongrid_pac
inverter_pac_microgrid	watts	 offgrid_pac	 offgrid_pac
battery_min_cell_temp	celcius	 min_battery_temp	 min_battery_temp
battery_max_cell_temp	celcius	 max_battery_temp	 max_battery_temp
state_bms	string		state_bms
state_inverter	string		state_inverter
system_status_timestamp	timestamp	status_timestamp	status_timestamp
fully_charged_at	timestamp		fully_charged_at
fully_discharged_at	timestamp		fully_discharged_at
backup_reserve_at	timestamp		backup_reserve_at
last_time_full	timestamp		last_time_full
last_updated	timestamp		last_updated
status_battery_charging	bool	 charging	 charging
status_battery_discharging	bool	 discharging	 discharging
configuration_em_operatingmode	enum	 operating_mode	 operating_mode
```

Some sensors have enumerated values:

```
system_status: ["Config", "OnGrid", "OffGrid", "Critical Error"]
sonnenbackup_state: ["standby", "charging", "discharging", "discharging reserve", "charged", "discharged"]
operating_mode: {1: "Manual",2: "Automatic",6: "Extension module",10: "Time of Use"}


```

sonnenbackup_state "standby" indicates the battery is neither charging or discharging.
The battery could be fully charged, fully discharged, at reserve limit or no production available to charge.
Must be read in conjuction with "relative_state_of_charge" to determine the reason for "standby".

Timestamps for fully charged, fully discharged & backup reserve, are calculated on current consumption/production.
When battery is in standby, these timestamp values are undefined, as will some when charging/discharging.
Times are calculated relative to hass server time, which should match "system_status_timestamp"

## Confirmed Supported Batteries

These batteries have been tested and confirmed to be working. If your batterie is not listed below, this library may still work provided your battery admin portal can generate an API read token and responds to Sonnen API V2 endpoints.

* Power unit Evo IP56
